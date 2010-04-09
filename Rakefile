task :default do
  `rm -rf jekyll`
  `cp -r site jekyll`

  # generate recipe pages
  Dir['recipes/*/recipe.md'].each do |source|
    dest = source.sub('recipes', 'jekyll').sub('/recipe.md', '.markdown')
    puts "-- #{dest}"
    open(dest, 'w') do |out|
      out.write open(source.sub('/recipe.md', '/meta.yml')).read()
      out.write "layout: default\n"
      out.write "---\n"
      out.write open(source).read()
    end
  end
end
