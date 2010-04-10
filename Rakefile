require 'rubygems'
require 'rdiscount'
require 'liquid'

task :default do
  # cleanup
  `rm -rf www; mkdir www; cp site/*.css www`
  
  # generate recipe pages
  layout = Liquid::Template.parse(open('site/layout.liquid').read())
  recipes = Dir['recipes/*/recipe.md'].map do |source|
    next if source =~ /a_sample_recipe/
    dest = source.sub('recipes', 'www').sub('/recipe.md', '.html')
    puts dest
    open(dest, 'w') do |out|
      content = RDiscount.new(open(source).read()).to_html
      out.write layout.render('content' => content)
    end
    recipe = dest.split('/').last
    title = recipe.sub('.html', '').split('_').map { |x| x.capitalize }.join(' ')
    { 'title' => title, 'href' => recipe }
  end.compact
  
  # generate index page
  index = Liquid::Template.parse(open('site/index.liquid').read())
  dest = 'www/index.html'
  puts dest
  open(dest, 'w') do |out|
    content = index.render('recipes' => recipes)
    out.write layout.render('content' => content)
  end
end
