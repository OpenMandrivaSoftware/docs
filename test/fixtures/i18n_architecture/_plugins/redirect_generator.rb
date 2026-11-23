# frozen_string_literal: true

root_file = File.join(Dir.pwd, '_plugins', 'redirect_generator.rb')
require root_file if File.file?(root_file)
