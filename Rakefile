require 'rubygems'
require 'rdiscount'
require 'liquid'
require 'yaml'

task :default do
  # copy static stuff
  `rm -rf www
  mkdir www
  cp -r site/* www
  rm -rf www/_*`
  
  # generate recipe pages
  layout = Liquid::Template.parse(open('site/_views/layout.liquid').read())
  recipes = Dir['recipes/*/*/recipe.md'].map do |source|
    meta = YAML.load(open(source.sub('/recipe.md', '/meta.yml')).read())
    name = source.split('/')[-2] + '.html'
    puts dest = "www/#{name}"
    open(dest, 'w') do |out|
      content = RDiscount.new(open(source).read()).to_html
      out.write layout.render('meta' => meta, 'content' => content)
    end
    { 'title' => meta['title'], 'href' => name }
  end.compact
  
  # generate index page
  index = Liquid::Template.parse(open('site/_views/index.liquid').read())
  puts dest = 'www/index.html'
  open(dest, 'w') do |out|
    content = index.render('recipes' => recipes)
    meta = { 'title' => 'Recipes' }
    out.write layout.render('meta' => meta, 'content' => content)
  end
end
