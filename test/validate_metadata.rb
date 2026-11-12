#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
require 'json'
require 'set'
require 'pathname'
require 'optparse'

# Authoritative multilingual metadata validator for OpenMandriva Docs.
# Validates frontmatter schema, language configuration, hierarchy integrity,
# and routing consistency across all documentation source variants.
class MetadataValidator
  REQUIRED_FIELDS = %w[page_id lang source_lang title permalink nav_order].freeze

  attr_reader :repo_root, :config, :languages, :default_lang, :excludes, :errors, :warnings

  def initialize(repo_root: Dir.pwd, config: nil)
    @repo_root = Pathname.new(repo_root)
    @config = config || load_config
    @languages = (@config['languages'] || ['en']).map(&:to_s)
    @default_lang = (@config['default_lang'] || 'en').to_s
    @excludes = (@config['exclude'] || []).map { |e| e.to_s.sub(%r{/+$}, '') }
    @errors = []
    @warnings = []
  end

  def load_config
    config_file = @repo_root.join('_config.yml')
    if config_file.file?
      YAML.load_file(config_file) || {}
    else
      { 'languages' => ['en', 'fr'], 'default_lang' => 'en', 'exclude' => [] }
    end
  end

  # Discover all markdown documentation files respecting Jekyll discovery rules and excludes.
  def discover_documents(search_root = @repo_root)
    docs = []
    Dir.glob(search_root.join('**/*.md')).sort.each do |fpath|
      path = Pathname.new(fpath)
      rel = path.relative_path_from(@repo_root).to_s

      # Exclude hidden directories, test artifacts, build destinations, vendor
      next if rel.start_with?('.', 'test/', '_site/', 'vendor/')
      next if path.each_filename.any? { |segment| segment.start_with?('.') }

      # Respect configured _config.yml excludes
      next if @excludes.any? { |ex| rel == ex || rel.start_with?("#{ex}/") }

      docs << path
    end
    docs
  end

  # Parse YAML frontmatter from a markdown file.
  def parse_frontmatter(path)
    rel_path = path.is_a?(Pathname) ? path.relative_path_from(@repo_root).to_s : path.to_s
    content = File.read(path, encoding: 'UTF-8')
    match = content.match(/\A---\s*\r?\n(.*?)\r?\n---\s*\r?\n/m)
    unless match
      @errors << "#{rel_path}: Missing valid YAML frontmatter block (file must begin with '---')"
      return nil
    end

    fm = YAML.safe_load(match[1])
    unless fm.is_a?(Hash)
      @errors << "#{rel_path}: Frontmatter is not a valid YAML mapping/hash"
      return nil
    end

    fm
  rescue Psych::SyntaxError => e
    rel_path = path.is_a?(Pathname) ? path.relative_path_from(@repo_root).to_s : path.to_s
    @errors << "#{rel_path}: YAML syntax error in frontmatter: #{e.message}"
    nil
  end

  # Load all parsed documents into a structured list.
  def load_documents(paths)
    parsed = []
    paths.each do |path|
      rel_path = path.relative_path_from(@repo_root).to_s
      fm = parse_frontmatter(path)
      next unless fm

      parsed << {
        path: path,
        rel_path: rel_path,
        frontmatter: fm,
        page_id: fm['page_id']&.to_s&.strip,
        parent_id: fm['parent_id']&.to_s&.strip,
        lang: fm['lang']&.to_s&.strip,
        source_lang: fm['source_lang']&.to_s&.strip,
        title: fm['title']&.to_s&.strip,
        permalink: fm['permalink']&.to_s&.strip,
        nav_order: fm['nav_order']
      }
    end
    parsed
  end

  # Calculate the effective public output route for a document variant.
  def effective_public_route(doc)
    permalink = doc[:permalink]
    return nil if permalink.nil? || permalink.empty?

    lang = doc[:lang]
    if lang == @default_lang
      permalink
    elsif permalink.start_with?("/#{lang}/")
      permalink
    else
      "/#{lang}#{permalink}"
    end
  end

  # Main validation entry point: checks schema, integrity, and routing rules.
  def validate(paths = nil)
    @errors.clear
    @warnings.clear

    doc_paths = paths ? paths.map { |p| Pathname.new(p) } : discover_documents
    docs = load_documents(doc_paths)

    # 1. Validate individual document frontmatter schema
    docs.each do |doc|
      validate_document_schema(doc)
    end

    # 2. Validate collection-wide uniqueness and hierarchy
    validate_uniqueness(docs)
    validate_translation_consistency(docs)
    validate_source_variants_existence(docs)
    validate_hierarchy(docs)
    validate_route_conflicts(docs)

    @errors.empty?
  end

  # Validate individual document schema requirements
  def validate_document_schema(doc)
    fm = doc[:frontmatter]
    rel = doc[:rel_path]

    # Required fields presence and non-emptiness
    REQUIRED_FIELDS.each do |field|
      val = fm[field]
      if val.nil? || (val.is_a?(String) && val.strip.empty?)
        @errors << "#{rel}: Missing or empty required metadata field '#{field}'"
      end
    end

    # Valid lang and source_lang against configured languages
    if doc[:lang] && !@languages.include?(doc[:lang])
      @errors << "#{rel}: Invalid lang '#{doc[:lang]}'. Allowed languages from _config.yml: #{@languages.inspect}"
    end

    if doc[:source_lang] && !@languages.include?(doc[:source_lang])
      @errors << "#{rel}: Invalid source_lang '#{doc[:source_lang]}'. Allowed languages from _config.yml: #{@languages.inspect}"
    end

    # Validate nav_order is strictly an Integer type (reject floats, strings, booleans)
    val_order = fm['nav_order']
    unless val_order.nil?
      unless val_order.is_a?(Integer)
        @errors << "#{rel}: Field 'nav_order' must be an integer, got #{val_order.class} (#{val_order.inspect})"
      end
    end

    # Validate permalink syntax
    permalink = doc[:permalink]
    if permalink
      unless permalink.start_with?('/')
        @errors << "#{rel}: Permalink must start with '/', got '#{permalink}'"
      end
      if permalink.match?(/\s/)
        @errors << "#{rel}: Permalink cannot contain whitespace: '#{permalink}'"
      end
      if permalink.include?('?') || permalink.include?('#')
        @errors << "#{rel}: Permalink cannot contain query parameters or fragments: '#{permalink}'"
      end
      # Reject language prefix in permalinks
      @languages.each do |lang|
        if permalink == "/#{lang}" || permalink.start_with?("/#{lang}/")
          @errors << "#{rel}: Permalink cannot start with language prefix '/#{lang}': '#{permalink}'"
        end
      end
    end
  end

  # Validate uniqueness of (page_id, lang)
  def validate_uniqueness(docs)
    seen = {}
    docs.each do |doc|
      next unless doc[:page_id] && doc[:lang]

      key = [doc[:page_id], doc[:lang]]
      if seen.key?(key)
        @errors << "#{doc[:rel_path]}: Duplicate page_id '#{doc[:page_id]}' for language '#{doc[:lang]}' (already defined in '#{seen[key]}')"
      else
        seen[key] = doc[:rel_path]
      end
    end
  end

  # Validate consistency across translations of the same page_id
  def validate_translation_consistency(docs)
    by_page_id = docs.group_by { |d| d[:page_id] }

    by_page_id.each do |pid, variants|
      next if pid.nil? || variants.size <= 1

      first = variants.first
      variants[1..].each do |other|
        # source_lang must match
        if first[:source_lang] && other[:source_lang] && first[:source_lang] != other[:source_lang]
          @errors << "Translation inconsistency for page_id '#{pid}': '#{first[:rel_path]}' has source_lang '#{first[:source_lang]}', but '#{other[:rel_path]}' has '#{other[:source_lang]}'"
        end

        # parent_id must match
        first_parent = first[:parent_id].to_s.strip
        other_parent = other[:parent_id].to_s.strip
        if first_parent != other_parent
          @errors << "Translation inconsistency for page_id '#{pid}': '#{first[:rel_path]}' has parent_id '#{first_parent.empty? ? 'nil' : first_parent}', but '#{other[:rel_path]}' has '#{other_parent.empty? ? 'nil' : other_parent}'"
        end

        # nav_order must match
        if first[:nav_order] != other[:nav_order]
          @errors << "Translation inconsistency for page_id '#{pid}': '#{first[:rel_path]}' has nav_order #{first[:nav_order]}, but '#{other[:rel_path]}' has #{other[:nav_order]}"
        end

        # permalink must be identical across translations
        if first[:permalink] != other[:permalink]
          @errors << "Translation inconsistency for page_id '#{pid}': '#{first[:rel_path]}' has permalink '#{first[:permalink]}', but '#{other[:rel_path]}' has '#{other[:permalink]}'"
        end
      end
    end
  end

  # Validate that the variant matching source_lang actually exists in the repository
  def validate_source_variants_existence(docs)
    by_page_id = docs.group_by { |d| d[:page_id] }

    by_page_id.each do |pid, variants|
      next if pid.nil?

      available_langs = variants.map { |v| v[:lang] }.to_set
      variants.each do |doc|
        src_lang = doc[:source_lang]
        next unless src_lang

        unless available_langs.include?(src_lang)
          @errors << "#{doc[:rel_path]}: Document declares source_lang '#{src_lang}', but no variant for language '#{src_lang}' exists in the repository for page_id '#{pid}'"
        end
      end
    end
  end

  # Validate hierarchy references, self-parenting, and cycles
  def validate_hierarchy(docs)
    all_page_ids = docs.map { |d| d[:page_id] }.compact.to_set
    parent_map = {}

    docs.each do |doc|
      pid = doc[:page_id]
      parent = doc[:parent_id]
      next if pid.nil? || parent.nil? || parent.empty?

      if parent == pid
        @errors << "#{doc[:rel_path]}: Document cannot have itself as parent_id ('#{parent}')"
        next
      end

      unless all_page_ids.include?(parent)
        @errors << "#{doc[:rel_path]}: Invalid parent_id '#{parent}': parent page_id not found in repository"
      end

      parent_map[pid] = parent
    end

    # Cycle detection
    parent_map.each_key do |start_id|
      visited = Set.new
      curr = start_id
      while parent_map.key?(curr)
        if visited.include?(curr)
          @errors << "Cyclic hierarchy detected involving page_id '#{curr}' starting from '#{start_id}'"
          break
        end
        visited.add(curr)
        curr = parent_map[curr]
      end
    end
  end

  # Normalizes a public URL into the actual output file path relative to _site root
  def output_file_for_route(route)
    p = route.to_s.sub(%r{^/+}, '')
    if p.empty? || p == 'index.html'
      'index.html'
    elsif p.end_with?('/')
      "#{p}index.html"
    else
      p
    end
  end

  # Validate that no two documents produce the same effective public output route or file
  def validate_route_conflicts(docs)
    files = {}
    by_page_id = docs.group_by { |d| d[:page_id] }

    docs.each do |doc|
      route = effective_public_route(doc)
      next unless route

      out_file = output_file_for_route(route)
      if files.key?(out_file)
        @errors << "Public route conflict: Both '#{doc[:rel_path]}' and '#{files[out_file][:doc]}' output to '#{route}'"
      else
        files[out_file] = { doc: doc[:rel_path], page_id: doc[:page_id], lang: doc[:lang] }
      end
    end

    # Check fallback routes for default_lang documents when non-default language has no translation
    docs.select { |d| d[:lang] == @default_lang }.each do |doc|
      variants = by_page_id[doc[:page_id]] || []
      existing_langs = variants.map { |v| v[:lang] }.to_set

      (@languages - [@default_lang]).each do |lang|
        next if existing_langs.include?(lang)

        fallback_route = doc[:permalink] == '/' ? "/#{lang}/" : "/#{lang}#{doc[:permalink]}"
        out_file = output_file_for_route(fallback_route)
        if files.key?(out_file) && files[out_file][:page_id] != doc[:page_id]
          @errors << "Fallback output conflict: Fallback for '#{doc[:rel_path]}' in '#{lang}' conflicts with '#{files[out_file][:doc]}' at '#{out_file}'"
        else
          files[out_file] = { doc: "#{doc[:rel_path]} (fallback #{lang})", page_id: doc[:page_id], lang: lang }
        end
      end
    end
  end

  # Migration retention validator: ensures all baseline logical documents and variants
  # from legacy_routes.json remain present in the current repository.
  def validate_migration_baseline(manifest_path = nil, paths = nil)
    manifest_file = Pathname.new(manifest_path || @repo_root.join('.agents/i18n-architecture/legacy_routes.json'))
    unless manifest_file.file?
      @errors << "Migration manifest not found at #{manifest_file}"
      return false
    end

    manifest = JSON.parse(File.read(manifest_file))
    routes = manifest['routes'] || []

    # Collect expected (page_id, actual_content_lang) for all actual documents (excluding system pages)
    expected_doc_variants = Set.new
    routes.each do |r|
      next if r['page_id'] == 'system.404'
      next if r['public_url'] == '/index.html' # root HTTP-equiv redirect stub
      expected_doc_variants.add([r['page_id'], r['actual_content_lang']])
    end

    doc_paths = paths ? paths.map { |p| Pathname.new(p) } : discover_documents
    docs = load_documents(doc_paths)
    actual_doc_variants = docs.map { |d| [d[:page_id], d[:lang]] }.to_set

    missing = expected_doc_variants - actual_doc_variants
    missing.each do |pid, lang|
      @errors << "Migration baseline violation: Missing required document variant for page_id '#{pid}' with lang '#{lang}'"
    end

    @errors.empty?
  end
end

# CLI executable entry point
if __FILE__ == $PROGRAM_NAME
  check_migration = false
  manifest_path = nil

  OptionParser.new do |opts|
    opts.banner = 'Usage: ruby test/validate_metadata.rb [options]'
    opts.on('--check-migration [MANIFEST]', 'Verify that all baseline migration documents remain present') do |m|
      check_migration = true
      manifest_path = m if m
    end
    opts.on('-h', '--help', 'Show help') do
      puts opts
      exit 0
    end
  end.parse!

  validator = MetadataValidator.new
  puts "Validating documentation source metadata against #{validator.repo_root}..."
  schema_valid = validator.validate

  migration_valid = true
  if check_migration
    puts 'Checking migration baseline retention...'
    migration_valid = validator.validate_migration_baseline(manifest_path)
  end

  if schema_valid && migration_valid
    puts "Validation PASSED: All source document metadata is valid and consistent."
    exit 0
  else
    puts "Validation FAILED with #{validator.errors.size} error(s):"
    validator.errors.each do |err|
      puts "  - #{err}"
    end
    exit 1
  end
end
