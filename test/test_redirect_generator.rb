# frozen_string_literal: true

require 'minitest/autorun'

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
end

require_relative '../_plugins/redirect_generator'

class TestRedirectGenerator < Minitest::Test
  DummyPage = Struct.new(:url, :data)

  DummySite = Struct.new(:config, :pages, :active_lang, :default_lang, :source)

  def setup
    @generator = OpenMandrivaDocs::RedirectGenerator.new
  end

  def test_generates_english_redirect
    page = DummyPage.new('/community/about-openmandriva/', {
      'redirect_from' => ['/community/about-openmandriva.en.html']
    })
    site = DummySite.new(
      { 'baseurl' => '' },
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

    content = redirect.content
    assert_includes content, '<link rel="canonical" href="/community/about-openmandriva/">'
    assert_includes content, '<meta http-equiv="refresh" content="0; url=/community/about-openmandriva/">'
    assert_includes content, 'var target = "/community/about-openmandriva/";'
    assert_includes content, 'window.location.replace(target + window.location.search + window.location.hash);'
  end

  def test_generates_french_translation_redirect
    page = DummyPage.new('/getting-started/downloading-openmandriva/', {
      'redirect_from' => ['/getting-started/downloading-openmandriva.fr.html']
    })
    site = DummySite.new(
      { 'baseurl' => '' },
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
  end

  def test_generates_french_fallback_redirect
    page = DummyPage.new('/community/chat-with-openmandriva/', {
      'redirect_from' => ['/community/chat-with-openmandriva.en.html']
    })
    site = DummySite.new(
      { 'baseurl' => '' },
      [page],
      'fr',
      'en',
      '/tmp'
    )

    @generator.generate(site)

    assert_equal 2, site.pages.length
    redirect = site.pages.last
    assert_equal '/community', redirect.dir
    assert_equal 'chat-with-openmandriva.en.html', redirect.name
    assert_equal '/fr/community/chat-with-openmandriva/', redirect.data['redirect']['to']
    assert_includes redirect.content, '<meta http-equiv="refresh" content="0; url=/fr/community/chat-with-openmandriva/">'
  end

  def test_baseurl_handling_empty_and_prefixed
    page = DummyPage.new('/community/about-openmandriva/', {
      'redirect_from' => ['/community/about-openmandriva.en.html']
    })
    site = DummySite.new(
      { 'baseurl' => '/docs' },
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

  def test_root_homepage_redirect
    page = DummyPage.new('/', {
      'redirect_from' => ['/index.en.html']
    })
    site = DummySite.new(
      { 'baseurl' => '' },
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

  def test_prevents_self_redirect_loops
    page = DummyPage.new('/', {
      'redirect_from' => ['/', '/index.html']
    })
    site = DummySite.new(
      { 'baseurl' => '' },
      [page],
      'en',
      'en',
      '/tmp'
    )

    @generator.generate(site)

    # Self-redirects must be skipped
    assert_equal 1, site.pages.length
  end

  def test_prevents_collision_with_existing_output_pages
    page1 = DummyPage.new('/existing.html', {})
    page2 = DummyPage.new('/other/', {
      'redirect_from' => ['/existing.html']
    })
    site = DummySite.new(
      { 'baseurl' => '' },
      [page1, page2],
      'en',
      'en',
      '/tmp'
    )

    @generator.generate(site)

    # Collision with existing page1 must be skipped
    assert_equal 2, site.pages.length
  end
end
