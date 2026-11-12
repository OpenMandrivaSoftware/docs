# frozen_string_literal: true

require 'minitest/autorun'
require 'pathname'
require 'tmpdir'
require_relative 'validate_metadata'

class TestMetadataValidator < Minitest::Test
  def setup
    @repo_root = Pathname.new(File.expand_path('..', __dir__))
  end

  def test_production_repository_is_valid
    validator = MetadataValidator.new(repo_root: @repo_root)
    valid = validator.validate
    assert valid, "Production repository failed metadata validation:\n#{validator.errors.join("\n")}"
    assert_empty validator.errors

    migration_valid = validator.validate_migration_baseline
    assert migration_valid, "Production repository violated migration baseline:\n#{validator.errors.join("\n")}"
  end

  def create_fixture_doc(dir, rel_path, frontmatter, body = 'Content')
    fpath = Pathname.new(dir).join(rel_path)
    fpath.parent.mkpath
    content = "---\n#{YAML.dump(frontmatter)}---\n#{body}\n"
    File.write(fpath, content)
    fpath
  end

  def test_valid_new_language_variant
    Dir.mktmpdir do |tmp|
      tmp_path = Pathname.new(tmp)
      config = {
        'languages' => %w[en fr de ru],
        'default_lang' => 'en',
        'exclude' => []
      }
      validator = MetadataValidator.new(repo_root: tmp_path, config: config)

      create_fixture_doc(tmp, 'user-guide/index.en.md', {
        'page_id' => 'user-guide',
        'lang' => 'en',
        'source_lang' => 'en',
        'title' => 'User Guide EN',
        'permalink' => '/user-guide/',
        'nav_order' => 10
      })

      # Add new German translation
      create_fixture_doc(tmp, 'user-guide/index.de.md', {
        'page_id' => 'user-guide',
        'lang' => 'de',
        'source_lang' => 'en',
        'title' => 'Benutzerhandbuch DE',
        'permalink' => '/user-guide/',
        'nav_order' => 10
      })

      # Add new Russian translation
      create_fixture_doc(tmp, 'user-guide/index.ru.md', {
        'page_id' => 'user-guide',
        'lang' => 'ru',
        'source_lang' => 'en',
        'title' => 'Руководство пользователя RU',
        'permalink' => '/user-guide/',
        'nav_order' => 10
      })

      assert validator.validate, "Validator rejected valid new translations:\n#{validator.errors.join("\n")}"
      assert_empty validator.errors
    end
  end

  def test_missing_required_metadata
    Dir.mktmpdir do |tmp|
      tmp_path = Pathname.new(tmp)
      validator = MetadataValidator.new(repo_root: tmp_path, config: { 'languages' => ['en'], 'default_lang' => 'en' })

      create_fixture_doc(tmp, 'article/index.en.md', {
        'lang' => 'en',
        'source_lang' => 'en',
        'title' => 'Incomplete article',
        'permalink' => '/article/',
        'nav_order' => 10
        # Missing page_id
      })

      refute validator.validate
      assert validator.errors.any? { |e| e.include?("Missing or empty required metadata field 'page_id'") }
    end
  end

  def test_invalid_language
    Dir.mktmpdir do |tmp|
      tmp_path = Pathname.new(tmp)
      config = { 'languages' => %w[en fr], 'default_lang' => 'en' }
      validator = MetadataValidator.new(repo_root: tmp_path, config: config)

      create_fixture_doc(tmp, 'article/index.es.md', {
        'page_id' => 'article',
        'lang' => 'es', # Not in ['en', 'fr']
        'source_lang' => 'en',
        'title' => 'Spanish article',
        'permalink' => '/article.es.html',
        'nav_order' => 10
      })

      refute validator.validate
      assert validator.errors.any? { |e| e.include?("Invalid lang 'es'") }
    end
  end

  def test_duplicate_page_id_and_lang
    Dir.mktmpdir do |tmp|
      tmp_path = Pathname.new(tmp)
      validator = MetadataValidator.new(repo_root: tmp_path, config: { 'languages' => ['en'], 'default_lang' => 'en' })

      create_fixture_doc(tmp, 'doc1/index.en.md', {
        'page_id' => 'duplicate.id',
        'lang' => 'en',
        'source_lang' => 'en',
        'title' => 'Doc 1',
        'permalink' => '/doc1/',
        'nav_order' => 10
      })

      create_fixture_doc(tmp, 'doc2/index.en.md', {
        'page_id' => 'duplicate.id',
        'lang' => 'en',
        'source_lang' => 'en',
        'title' => 'Doc 2',
        'permalink' => '/doc2/',
        'nav_order' => 20
      })

      refute validator.validate
      assert validator.errors.any? { |e| e.include?("Duplicate page_id 'duplicate.id' for language 'en'") }
    end
  end

  def test_missing_source_variant
    Dir.mktmpdir do |tmp|
      tmp_path = Pathname.new(tmp)
      config = { 'languages' => %w[en fr], 'default_lang' => 'en' }
      validator = MetadataValidator.new(repo_root: tmp_path, config: config)

      create_fixture_doc(tmp, 'article/index.fr.md', {
        'page_id' => 'orphaned.article',
        'lang' => 'fr',
        'source_lang' => 'en', # No en variant exists!
        'title' => 'Article FR',
        'permalink' => '/article.fr.html',
        'nav_order' => 10
      })

      refute validator.validate
      assert validator.errors.any? { |e| e.include?("declares source_lang 'en', but no variant for language 'en' exists") }
    end
  end

  def test_inconsistent_parent_id_between_translations
    Dir.mktmpdir do |tmp|
      tmp_path = Pathname.new(tmp)
      config = { 'languages' => %w[en fr], 'default_lang' => 'en' }
      validator = MetadataValidator.new(repo_root: tmp_path, config: config)

      create_fixture_doc(tmp, 'parent-a/index.en.md', {
        'page_id' => 'parent.a', 'lang' => 'en', 'source_lang' => 'en',
        'title' => 'Parent A', 'permalink' => '/parent-a/', 'nav_order' => 1
      })
      create_fixture_doc(tmp, 'parent-b/index.en.md', {
        'page_id' => 'parent.b', 'lang' => 'en', 'source_lang' => 'en',
        'title' => 'Parent B', 'permalink' => '/parent-b/', 'nav_order' => 2
      })

      create_fixture_doc(tmp, 'child/index.en.md', {
        'page_id' => 'child.doc', 'parent_id' => 'parent.a', 'lang' => 'en', 'source_lang' => 'en',
        'title' => 'Child EN', 'permalink' => '/child/', 'nav_order' => 10
      })
      create_fixture_doc(tmp, 'child/index.fr.md', {
        'page_id' => 'child.doc', 'parent_id' => 'parent.b', 'lang' => 'fr', 'source_lang' => 'en',
        'title' => 'Child FR', 'permalink' => '/child.fr.html', 'nav_order' => 10
      })

      refute validator.validate
      assert validator.errors.any? { |e| e.include?("Translation inconsistency for page_id 'child.doc'") }
    end
  end

  def test_hierarchy_cycle_and_self_parent
    Dir.mktmpdir do |tmp|
      tmp_path = Pathname.new(tmp)
      validator = MetadataValidator.new(repo_root: tmp_path, config: { 'languages' => ['en'], 'default_lang' => 'en' })

      create_fixture_doc(tmp, 'self/index.en.md', {
        'page_id' => 'self.doc', 'parent_id' => 'self.doc', 'lang' => 'en', 'source_lang' => 'en',
        'title' => 'Self Parent', 'permalink' => '/self/', 'nav_order' => 1
      })

      refute validator.validate
      assert validator.errors.any? { |e| e.include?("cannot have itself as parent_id ('self.doc')") }
    end

    Dir.mktmpdir do |tmp|
      tmp_path = Pathname.new(tmp)
      validator = MetadataValidator.new(repo_root: tmp_path, config: { 'languages' => ['en'], 'default_lang' => 'en' })

      create_fixture_doc(tmp, 'a/index.en.md', {
        'page_id' => 'cycle.a', 'parent_id' => 'cycle.b', 'lang' => 'en', 'source_lang' => 'en',
        'title' => 'Cycle A', 'permalink' => '/a/', 'nav_order' => 1
      })
      create_fixture_doc(tmp, 'b/index.en.md', {
        'page_id' => 'cycle.b', 'parent_id' => 'cycle.c', 'lang' => 'en', 'source_lang' => 'en',
        'title' => 'Cycle B', 'permalink' => '/b/', 'nav_order' => 1
      })
      create_fixture_doc(tmp, 'c/index.en.md', {
        'page_id' => 'cycle.c', 'parent_id' => 'cycle.a', 'lang' => 'en', 'source_lang' => 'en',
        'title' => 'Cycle C', 'permalink' => '/c/', 'nav_order' => 1
      })

      refute validator.validate
      assert validator.errors.any? { |e| e.include?("Cyclic hierarchy detected involving page_id 'cycle.a'") }
    end
  end

  def test_invalid_nav_order
    Dir.mktmpdir do |tmp|
      tmp_path = Pathname.new(tmp)
      validator = MetadataValidator.new(repo_root: tmp_path, config: { 'languages' => ['en'], 'default_lang' => 'en' })

      create_fixture_doc(tmp, 'article/index.en.md', {
        'page_id' => 'bad.order',
        'lang' => 'en',
        'source_lang' => 'en',
        'title' => 'Bad Order',
        'permalink' => '/article/',
        'nav_order' => 'first' # Not an integer
      })

      refute validator.validate
      assert validator.errors.any? { |e| e.include?("Field 'nav_order' must be an integer") }
    end
  end

  def test_conflicting_routes
    Dir.mktmpdir do |tmp|
      tmp_path = Pathname.new(tmp)
      validator = MetadataValidator.new(repo_root: tmp_path, config: { 'languages' => ['en'], 'default_lang' => 'en' })

      create_fixture_doc(tmp, 'article1/index.en.md', {
        'page_id' => 'article.one', 'lang' => 'en', 'source_lang' => 'en',
        'title' => 'Article 1', 'permalink' => '/same-route/', 'nav_order' => 1
      })
      create_fixture_doc(tmp, 'article2/index.en.md', {
        'page_id' => 'article.two', 'lang' => 'en', 'source_lang' => 'en',
        'title' => 'Article 2', 'permalink' => '/same-route/', 'nav_order' => 2
      })

      refute validator.validate
      assert validator.errors.any? { |e| e.include?("Public route conflict: Both 'article2/index.en.md' and 'article1/index.en.md' output to '/same-route/'") }
    end
  end

  def test_migration_baseline_detects_missing_document
    Dir.mktmpdir do |tmp|
      tmp_path = Pathname.new(tmp)
      manifest_path = tmp_path.join('legacy_routes.json')
      File.write(manifest_path, JSON.generate({
        'routes' => [
          { 'page_id' => 'doc.alpha', 'actual_content_lang' => 'en', 'public_url' => '/alpha.en.html' },
          { 'page_id' => 'doc.beta', 'actual_content_lang' => 'en', 'public_url' => '/beta.en.html' }
        ]
      }))

      validator = MetadataValidator.new(repo_root: tmp_path, config: { 'languages' => ['en'], 'default_lang' => 'en' })

      # Only create alpha, omit beta
      create_fixture_doc(tmp, 'alpha/index.en.md', {
        'page_id' => 'doc.alpha', 'lang' => 'en', 'source_lang' => 'en',
        'title' => 'Doc Alpha', 'permalink' => '/alpha.en.html', 'nav_order' => 1
      })

      refute validator.validate_migration_baseline(manifest_path.to_s)
      assert validator.errors.any? { |e| e.include?("Missing required document variant for page_id 'doc.beta'") }
    end
  end
end
