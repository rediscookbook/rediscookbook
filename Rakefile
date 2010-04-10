require 'rubygems'
require 'rdiscount'
require 'liquid'
require 'yaml'

task :default do
  # cleanup
  `rm -rf www; mkdir www; cp site/*.css www`
  
  # generate recipe pages
  layout = Liquid::Template.parse(open('site/layout.liquid').read())
  recipes = Dir['recipes/*/recipe.md'].map do |source|
    next if source =~ /a_sample_recipe/
    meta = YAML.load(open(source.sub('/recipe.md', '/meta.yml')).read())
    puts dest = source.sub('recipes', 'www').sub('/recipe.md', '.html')
    open(dest, 'w') do |out|
      content = RDiscount.new(open(source).read()).to_html
      out.write layout.render('meta' => meta, 'content' => content)
    end
    { 'title' => meta['title'], 'href' => dest.split('/').last }
  end.compact
  
  # generate index page
  index = Liquid::Template.parse(open('site/index.liquid').read())
  puts dest = 'www/index.html'
  open(dest, 'w') do |out|
    content = index.render('recipes' => recipes)
    meta = { 'title' => 'Recipes' }
    out.write layout.render('meta' => meta, 'content' => content)
  end
end
