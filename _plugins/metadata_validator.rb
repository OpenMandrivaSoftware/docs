# frozen_string_literal: true

# OpenMandriva Documentation - Metadata Schema Validator
# Validates page_id uniqueness, parent_id existence, and metadata integrity at build time.

Jekyll::Hooks.register :site, :post_read do |site|
  doc_pages = site.pages.select { |p| p.data['page_id'] }
  next if doc_pages.empty?

  page_ids_by_lang = Hash.new { |h, k| h[k] = {} }
  all_page_ids = Set.new

  doc_pages.each do |page|
    pid = page.data['page_id'].to_s.strip
    lang = (page.data['lang'] || 'en').to_s.strip

    if pid.empty?
      raise "MetadataValidationError: Empty page_id in #{page.relative_path}"
    end

    all_page_ids.add(pid)

    if page_ids_by_lang[lang].key?(pid)
      existing_path = page_ids_by_lang[lang][pid]
      raise "MetadataValidationError: Duplicate page_id '#{pid}' for language '#{lang}' found in #{page.relative_path} (already defined in #{existing_path})"
    end
    page_ids_by_lang[lang][pid] = page.relative_path
  end

  # Validate parent_id references
  doc_pages.each do |page|
    parent_id = page.data['parent_id']
    next if parent_id.nil? || parent_id.to_s.strip.empty?

    parent_str = parent_id.to_s.strip
    if parent_str == page.data['page_id'].to_s.strip
      raise "MetadataValidationError: Document '#{page.relative_path}' cannot have itself as parent_id ('#{parent_str}')"
    end

    unless all_page_ids.include?(parent_str)
      raise "MetadataValidationError: Invalid parent_id '#{parent_str}' in #{page.relative_path}: parent page_id does not exist"
    end
  end
end
