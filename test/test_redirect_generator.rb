# frozen_string_literal: true

require 'minitest/autorun'
require 'json'
require 'tempfile'

# Minimal Jekyll Page stub if Jekyll is not loaded
module Jekyll
  class Page
    attr_accessor :site, :base, :dir, :name, :data, :content

    def process(name)
      @name = name
    end
  end

  class Generator
    def self.safe(val = nil); end
    def self.priority(val = nil); end
  end

  class Hooks
    def self.register(*_args); end
  end
end

require_relative '../_plugins/redirect_generator'

class TestRedirectGenerator < Minitest::Test
  DummyPage = Struct.new(:url, :data)

  DummySite = Struct.new(:config, :pages, :active_lang, :default_lang, :source)

  def setup
    @generator = OpenMandrivaDocs::RedirectGenerator.new
  end

  def with_manifest(routes)
    file = Tempfile.new(['legacy_routes_', '.json'])
    file.write(JSON.pretty_generate({ 'routes' => routes }))
    file.close
    yield file.path
  ensure
    file.unlink if file
  end

  def test_generates_english_redirect_with_exclusion_metadata
    routes = [
      {
        'page_id' => 'community.about-openmandriva',
        'requested_locale' => 'en',
        'public_url' => '/community/about-openmandriva.en.html',
        'canonical_destination' => '/community/about-openmandriva/'
      }
    ]

    with_manifest(routes) do |manifest_path|
      page = DummyPage.new('/community/about-openmandriva/', {
        'page_id' => 'community.about-openmandriva'
      })
      site = DummySite.new(
        { 'baseurl' => '', 'legacy_routes_path' => manifest_path },
        [page],
        'en',
        'en',
        '/tmp'
      )

      @generator.generate(site)

      assert_equal 2, site.pages.length
      redirect = site.pages.last
      assert_instance_of OpenMandrivaDocs::RedirectPage, redirect
      assert_equal '/community', redirect.dir
      assert_equal 'about-openmandriva.en.html', redirect.name
      assert_equal '/community/about-openmandriva/', redirect.data['redirect']['to']

      # Verify exclusion metadata to keep redirects out of nav & search
      assert_equal true, redirect.data['nav_exclude']
      assert_equal true, redirect.data['search_exclude']
      assert_equal false, redirect.data['sitemap']
      assert_equal 'noindex', redirect.data['robots']

      content = redirect.content
      assert_includes content, '<meta name="robots" content="noindex">'
      assert_includes content, '<link rel="canonical" href="/community/about-openmandriva/">'
      assert_includes content, '<meta http-equiv="refresh" content="0; url=/community/about-openmandriva/">'
      assert_includes content, 'var target = "/community/about-openmandriva/";'
      assert_includes content, 'window.location.replace(target + window.location.search + window.location.hash);'
    end
  end

  def test_generates_french_translation_redirect
    routes = [
      {
        'page_id' => 'getting-started.downloading-openmandriva',
        'requested_locale' => 'fr',
        'public_url' => '/fr/getting-started/downloading-openmandriva.fr.html',
        'canonical_destination' => '/fr/getting-started/downloading-openmandriva/'
      }
    ]

    with_manifest(routes) do |manifest_path|
      page = DummyPage.new('/getting-started/downloading-openmandriva/', {
        'page_id' => 'getting-started.downloading-openmandriva'
      })
      site = DummySite.new(
        { 'baseurl' => '', 'legacy_routes_path' => manifest_path },
        [page],
        'fr',
        'en',
        '/tmp'
      )

      @generator.generate(site)

      assert_equal 2, site.pages.length
      redirect = site.pages.last
      assert_equal '/getting-started', redirect.dir
      assert_equal 'downloading-openmandriva.fr.html', redirect.name
      assert_equal '/fr/getting-started/downloading-openmandriva/', redirect.data['redirect']['to']
      assert_includes redirect.content, '<link rel="canonical" href="/fr/getting-started/downloading-openmandriva/">'
      assert_includes redirect.content, '<meta name="robots" content="noindex">'
    end
  end

  def test_generates_french_fallback_redirect_independent_of_source_metadata
    routes = [
      {
        'page_id' => 'user-guide.first-steps',
        'requested_locale' => 'fr',
        'public_url' => '/fr/user-guide/first-steps.en.html',
        'canonical_destination' => '/fr/user-guide/first-steps/'
      }
    ]

    with_manifest(routes) do |manifest_path|
      # Page has NO redirect_from frontmatter; it is an English fallback page in FR pass
      page = DummyPage.new('/user-guide/first-steps/', {
        'page_id' => 'user-guide.first-steps',
        'lang' => 'en'
      })
      site = DummySite.new(
        { 'baseurl' => '', 'legacy_routes_path' => manifest_path },
        [page],
        'fr',
        'en',
        '/tmp'
      )

      @generator.generate(site)

      assert_equal 2, site.pages.length
      redirect = site.pages.last
      assert_equal '/user-guide', redirect.dir
      assert_equal 'first-steps.en.html', redirect.name
      assert_equal '/fr/user-guide/first-steps/', redirect.data['redirect']['to']
      assert_includes redirect.content, '<link rel="canonical" href="/fr/user-guide/first-steps/">'
    end
  end

  def test_adding_real_translation_preserves_historical_fallback_url
    routes = [
      {
        'page_id' => 'user-guide.first-steps',
        'requested_locale' => 'fr',
        'public_url' => '/fr/user-guide/first-steps.en.html',
        'canonical_destination' => '/fr/user-guide/first-steps/'
      }
    ]

    with_manifest(routes) do |manifest_path|
      # When real French translation replaces English fallback, page.data['lang'] is 'fr'
      # and contains NO redirect_from metadata.
      page_fr = DummyPage.new('/user-guide/first-steps/', {
        'page_id' => 'user-guide.first-steps',
        'lang' => 'fr'
      })
      site = DummySite.new(
        { 'baseurl' => '', 'legacy_routes_path' => manifest_path },
        [page_fr],
        'fr',
        'en',
        '/tmp'
      )

      @generator.generate(site)

      # Historical French URL still exists and points to canonical French permalink
      assert_equal 2, site.pages.length
      redirect = site.pages.last
      assert_equal 'first-steps.en.html', redirect.name
      assert_equal '/fr/user-guide/first-steps/', redirect.data['redirect']['to']
    end
  end

  def test_baseurl_handling_empty_and_prefixed
    routes = [
      {
        'page_id' => 'community.about-openmandriva',
        'requested_locale' => 'fr',
        'public_url' => '/fr/community/about-openmandriva.en.html',
        'canonical_destination' => '/fr/community/about-openmandriva/'
      }
    ]

    with_manifest(routes) do |manifest_path|
      page = DummyPage.new('/community/about-openmandriva/', {
        'page_id' => 'community.about-openmandriva'
      })
      site = DummySite.new(
        { 'baseurl' => '/docs', 'legacy_routes_path' => manifest_path },
        [page],
        'fr',
        'en',
        '/tmp'
      )

      @generator.generate(site)

      redirect = site.pages.last
      assert_equal '/docs/fr/community/about-openmandriva/', redirect.data['redirect']['to']
      assert_includes redirect.content, 'href="/docs/fr/community/about-openmandriva/"'
      assert_includes redirect.content, 'var target = "/docs/fr/community/about-openmandriva/";'
    end
  end

  def test_root_homepage_redirect
    routes = [
      {
        'page_id' => 'home',
        'requested_locale' => 'en',
        'public_url' => '/index.en.html',
        'canonical_destination' => '/'
      }
    ]

    with_manifest(routes) do |manifest_path|
      page = DummyPage.new('/', {
        'page_id' => 'home'
      })
      site = DummySite.new(
        { 'baseurl' => '', 'legacy_routes_path' => manifest_path },
        [page],
        'en',
        'en',
        '/tmp'
      )

      @generator.generate(site)

      assert_equal 2, site.pages.length
      redirect = site.pages.last
      assert_equal '/', redirect.dir
      assert_equal 'index.en.html', redirect.name
      assert_equal '/', redirect.data['redirect']['to']
      assert_includes redirect.content, '<link rel="canonical" href="/">'
    end
  end

  def test_prevents_self_redirect_loops
    routes = [
      {
        'page_id' => 'home',
        'requested_locale' => 'en',
        'public_url' => '/index.html',
        'canonical_destination' => '/'
      },
      {
        'page_id' => 'home',
        'requested_locale' => 'fr',
        'public_url' => '/fr/index.html',
        'canonical_destination' => '/fr/'
      }
    ]

    with_manifest(routes) do |manifest_path|
      page_en = DummyPage.new('/', { 'page_id' => 'home' })
      site_en = DummySite.new(
        { 'baseurl' => '', 'legacy_routes_path' => manifest_path },
        [page_en],
        'en',
        'en',
        '/tmp'
      )

      @generator.generate(site_en)
      # Self-redirect /index.html -> / must be skipped
      assert_equal 1, site_en.pages.length

      page_fr = DummyPage.new('/', { 'page_id' => 'home' })
      site_fr = DummySite.new(
        { 'baseurl' => '', 'legacy_routes_path' => manifest_path },
        [page_fr],
        'fr',
        'en',
        '/tmp'
      )

      @generator.generate(site_fr)
      # Self-redirect /fr/index.html -> /fr/ must be skipped
      assert_equal 1, site_fr.pages.length
    end
  end

  def test_detects_collision_with_conflicting_page
    routes = [
      {
        'page_id' => 'doc.b',
        'requested_locale' => 'en',
        'public_url' => '/existing-doc.html',
        'canonical_destination' => '/doc-b/'
      }
    ]

    with_manifest(routes) do |manifest_path|
      # Existing page 'doc.a' already has url '/existing-doc.html'
      page_a = DummyPage.new('/existing-doc.html', { 'page_id' => 'doc.a' })
      page_b = DummyPage.new('/doc-b/', { 'page_id' => 'doc.b' })

      site = DummySite.new(
        { 'baseurl' => '', 'legacy_routes_path' => manifest_path },
        [page_a, page_b],
        'en',
        'en',
        '/tmp'
      )

      err = assert_raises(RuntimeError) do
        @generator.generate(site)
      end
      assert_includes err.message, "Redirect collision"
      assert_includes err.message, "conflicts with existing page"
    end
  end

  def test_detects_conflicting_redirect_destinations
    routes = [
      {
        'page_id' => 'doc.a',
        'requested_locale' => 'en',
        'public_url' => '/same-alias.html',
        'canonical_destination' => '/doc-a/'
      },
      {
        'page_id' => 'doc.b',
        'requested_locale' => 'en',
        'public_url' => '/same-alias.html',
        'canonical_destination' => '/doc-b/'
      }
    ]

    with_manifest(routes) do |manifest_path|
      page_a = DummyPage.new('/doc-a/', { 'page_id' => 'doc.a' })
      page_b = DummyPage.new('/doc-b/', { 'page_id' => 'doc.b' })

      site = DummySite.new(
        { 'baseurl' => '', 'legacy_routes_path' => manifest_path },
        [page_a, page_b],
        'en',
        'en',
        '/tmp'
      )

      err = assert_raises(RuntimeError) do
        @generator.generate(site)
      end
      assert_includes err.message, "Conflicting redirect destination"
    end
  end
end
