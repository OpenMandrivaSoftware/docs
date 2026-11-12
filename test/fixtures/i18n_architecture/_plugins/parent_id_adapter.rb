# Approach A: Resolve parent_id into native Just the Docs parent and grand_parent metadata
Jekyll::Hooks.register :site, :post_read, priority: :low do |site|
  pages_by_id = {}
  site.pages.each do |p|
    pid = p.data['page_id']
    pages_by_id[pid] = p if pid
  end

  site.pages.each do |p|
    parent_id = p.data['parent_id']
    if parent_id && (parent = pages_by_id[parent_id])
      p.data['parent'] = parent.data['title']
      if (g_id = parent.data['parent_id']) && (grand = pages_by_id[g_id])
        p.data['grand_parent'] = grand.data['title']
      end
    end
  end
end
