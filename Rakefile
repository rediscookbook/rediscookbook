require 'rubygems'
require 'rdiscount'
require 'erb'

task :default => [:build]

task :build do
  `rm -rf www; mkdir www; cp site/*.css www`

  layout = ERB.new(open('site/layout.erb').read())
  
  # generate recipe pages
  recipes = Dir['recipes/*/recipe.md'].map do |source|
    dest = source.sub('recipes', 'www').sub('/recipe.md', '.html')
    puts "-- #{dest}"
    open(dest, 'w') do |out|
      content = RDiscount.new(open(source).read()).to_html
      out.write layout.result(binding)
    end
    dest.split('/').last
  end
  
  # generate index page
  dest = 'www/index.html'
  puts "-- #{dest}"
  open(dest, 'w') do |out|
    index = ERB.new(open('site/index.erb').read())
    content = index.result(binding)
    out.write layout.result(binding)
  end
end
