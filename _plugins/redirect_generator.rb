# frozen_string_literal: true

require 'json'
require 'set'

module OpenMandrivaDocs
  # Represents a generated redirect HTML page with JavaScript fallback preserving
  # query strings and hash anchors, meta refresh, and canonical link.
  # Excluded from navigation and search indexing.
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
        'nav_exclude' => true,
        'search_exclude' => true,
        'redirect' => {
          'to' => target_url
        }
      }

      self.content = <<~HTML
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
          <meta name="robots" content="noindex">
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

    def url
      File.join(@dir, @name)
    end

    def destination(dest)
      File.join(dest, @dir, @name)
    end
  end

  # Generates static redirect HTML pages for legacy routes declared in
  # legacy_routes.json manifest, independent of translation availability.
  class RedirectGenerator < Jekyll::Generator
    safe true
    priority :low

    def generate(site)
      baseurl = site.config['baseurl'].to_s.chomp('/')
      active_lang = site.active_lang
      default_lang = site.default_lang || 'en'
      current_lang = active_lang || default_lang
      lang_prefix = (current_lang != default_lang) ? "/#{current_lang}" : ''

      # 1. Map existing canonical pages by page_id for fast lookup
      pages_by_id = {}
      existing_paths = {}

      site.pages.each do |p|
        pid = p.data['page_id']
        pages_by_id[pid] = p if pid
        norm_path = normalize_page_path(p.url)
        existing_paths[norm_path] = p.url
      end

      # 2. Locate and load legacy routes manifest
      routes = load_manifest(site)
      return if routes.empty?

      generated_redirects = []
      registered_redirects = {}

      routes.each do |r|
        # Skip canonical system/root pages that are generated directly from source templates
        next if r['page_id'] == 'system.404'
        next if r['public_url'] == '/index.html' || r['public_url'] == '/fr/index.html'

        req_locale = r['requested_locale'] || default_lang
        next unless req_locale == current_lang

        page_id = r['page_id']
        page = pages_by_id[page_id]

        # Determine canonical destination URL
        canonical_path = if page
                           page.url
                         elsif r['canonical_destination']
                           r['canonical_destination']
                         else
                           next
                         end

        canonical_target = format_target_url(baseurl, lang_prefix, canonical_path)

        # Legacy route public URL to preserve
        raw_url = r['public_url'].to_s.strip
        next if raw_url.empty?

        # Strip current_lang prefix if present (e.g. /fr/path -> /path)
        rel_path = raw_url
        if current_lang != default_lang
          rel_path = rel_path.delete_prefix("/#{current_lang}")
        end
        rel_path = "/#{rel_path}" unless rel_path.start_with?('/')

        normalized_redirect = normalize_page_path(rel_path)
        normalized_canonical = normalize_page_path(canonical_path)

        # Skip self-redirects
        next if normalized_redirect == normalized_canonical

        # Check collision with existing canonical page
        if existing_paths.key?(normalized_redirect)
          existing_target = existing_paths[normalized_redirect]
          # If it matches the canonical destination itself (e.g. /index.html -> / or /404.html), safe skip
          next if normalize_page_path(existing_target) == normalized_canonical

          raise "Redirect collision: legacy route '#{raw_url}' (#{normalized_redirect}) conflicts with existing page at '#{existing_target}'"
        end

        # Check collision with another redirect
        if registered_redirects.key?(normalized_redirect)
          prev_target = registered_redirects[normalized_redirect]
          if prev_target != canonical_target
            raise "Conflicting redirect destination for '#{normalized_redirect}': '#{prev_target}' vs '#{canonical_target}'"
          end
          next
        end

        dir, name = split_path(rel_path)
        redirect_page = RedirectPage.new(site, site.source, dir, name, canonical_target)
        generated_redirects << redirect_page
        registered_redirects[normalized_redirect] = canonical_target
      end

      site.pages.concat(generated_redirects)
    end

    def load_manifest(site)
      manifest_path = site.config['legacy_routes_path'] ||
                      File.join(site.source, '.agents', 'i18n-architecture', 'legacy_routes.json')

      return [] unless File.file?(manifest_path)

      data = JSON.parse(File.read(manifest_path, encoding: 'UTF-8'))
      data['routes'] || []
    rescue StandardError => e
      warn "RedirectGenerator: Failed to load legacy routes from #{manifest_path}: #{e.message}"
      []
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

# Ensure root-relative internal links and assets respect baseurl when configured
Jekyll::Hooks.register [:pages, :documents], :post_render do |doc|
  baseurl = doc.site.config['baseurl'].to_s.chomp('/')
  next if baseurl.empty?
  next if doc.output.nil?

  guard = Regexp.escape(baseurl.delete_prefix('/'))
  pattern = /(href|src)="\/(?!\/|#{guard}(?:\/|"|'|#|\?|$))/
  doc.output = doc.output.gsub(pattern) do |m|
    tag = m.start_with?('href') ? 'href' : 'src'
    "#{tag}=\"#{baseurl}/"
  end
end
