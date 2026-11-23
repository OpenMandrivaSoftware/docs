# Minimal Polyglot Fallback Adapter for deterministic source_lang resolution
module Jekyll
  class Site
    alias_method :coordinate_documents_polyglot_orig, :coordinate_documents

    def coordinate_documents(docs)
      # Sort documents in ascending fallback priority:
      # 0: other translations
      # 1: authoritative source variant (source_lang)
      # 2: default language ('en')
      # 3: requested locale (active_lang)
      sorted_docs = docs.sort_by do |doc|
        lang = doc.data['lang'] || derive_lang_from_path(doc) || @default_lang
        source_lang = doc.data['source_lang']

        priority = 0
        priority = 1 if source_lang && lang == source_lang
        priority = 2 if lang == @default_lang
        priority = 3 if lang == @active_lang
        priority
      end
      coordinate_documents_polyglot_orig(sorted_docs)
    end
  end
end
