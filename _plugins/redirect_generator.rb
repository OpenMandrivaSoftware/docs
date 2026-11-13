# frozen_string_literal: true

require 'json'
require 'set'

module OpenMandrivaDocs
  # Represents a generated redirect HTML page with JavaScript fallback preserving
  # query strings and hash anchors, meta refresh, and canonical link.
  class RedirectPage < Jekyll::Page
    def initialize(site, base, dir, name, target_url)
      @site = site
      @base = base
      @dir  = dir
      @name = name

      self.process(name)
      self.data = {
        'layout' => nil,
        'sitemap' => false,
        'robots' => 'noindex',
        'title' => 'Redirecting...',
        'redirect' => {
          'to' => target_url
        }
      }

      self.content = <<~HTML
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
          <title>Redirecting...</title>
          <link rel="canonical" href="#{target_url}">
          <meta http-equiv="refresh" content="0; url=#{target_url}">
          <script>
            (function() {
              var target = #{target_url.to_json};
              window.location.replace(target + window.location.search + window.location.hash);
            })();
          </script>
        </head>
        <body>
          <p>Redirecting to <a href="#{target_url}">#{target_url}</a>...</p>
        </body>
        </html>
      HTML
    end
  end

  # Generates static redirect HTML pages for legacy routes declared in
  # frontmatter `redirect_from`, respecting Polyglot active language and site baseurl.
  class RedirectGenerator < Jekyll::Generator
    safe true
    priority :low

    def generate(site)
      baseurl = site.config['baseurl'].to_s.chomp('/')
      active_lang = site.active_lang
      default_lang = site.default_lang || 'en'
      lang_prefix = (active_lang && active_lang != default_lang) ? "/#{active_lang}" : ''

      generated_redirects = []
      existing_paths = Set.new(site.pages.map { |p| normalize_page_path(p.url) })

      site.pages.each do |page|
        redirects = page.data['redirect_from']
        next if redirects.nil? || redirects.empty?

        redirects = [redirects] unless redirects.is_a?(Array)

        # Canonical destination URL for current language pass
        canonical_path = page.url
        canonical_target = format_target_url(baseurl, lang_prefix, canonical_path)

        redirects.each do |raw_redirect|
          redirect_path = raw_redirect.to_s.strip
          next if redirect_path.empty?

          # Strip active_lang prefix if present (e.g. /fr/path -> /path)
          if active_lang && active_lang != default_lang
            redirect_path = redirect_path.delete_prefix("/#{active_lang}")
          end
          redirect_path = "/#{redirect_path}" unless redirect_path.start_with?('/')

          # Self-redirect check: do not redirect to itself
          normalized_redirect = normalize_page_path(redirect_path)
          normalized_canonical = normalize_page_path(canonical_path)
          next if normalized_redirect == normalized_canonical

          # Prevent collision with real output pages in current pass
          next if existing_paths.include?(normalized_redirect)

          dir, name = split_path(redirect_path)
          redirect_page = RedirectPage.new(site, site.source, dir, name, canonical_target)
          generated_redirects << redirect_page
          existing_paths.add(normalized_redirect)
        end
      end

      site.pages.concat(generated_redirects)
    end

    def format_target_url(baseurl, lang_prefix, canonical_path)
      path = canonical_path.to_s.strip
      path = "/#{path}" unless path.start_with?('/')

      if path == '/'
        target = "#{baseurl}#{lang_prefix}/"
      else
        target = "#{baseurl}#{lang_prefix}#{path}"
      end
      target.empty? ? '/' : target
    end

    def normalize_page_path(path)
      p = path.to_s.strip
      p = "/#{p}" unless p.start_with?('/')
      if p == '/' || p == '/index.html'
        '/index.html'
      elsif p.end_with?('/')
        "#{p}index.html"
      else
        p
      end
    end

    def split_path(path)
      clean = path.start_with?('/') ? path[1..] : path
      if clean.end_with?('/')
        ["/#{clean.chomp('/')}", 'index.html']
      else
        dir = File.dirname(clean)
        dir = (dir == '.' || dir.empty?) ? '/' : "/#{dir}"
        name = File.basename(clean)
        [dir, name]
      end
    end
  end
end
