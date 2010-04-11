require 'rubygems'
require 'rdiscount'
require 'liquid'
require 'yaml'

# custom liquid tag to include code blocks
class CodeSnippet < Liquid::Tag
  def initialize(tag_name, filename, tokens)
     super 
     @filename = filename.strip
  end

  def render(context)
    out = StringIO.new
    open(@filename).each do |line|
      out.write "\t#{line}"
    end
    out.string
  end    
end

Liquid::Template.register_tag('code_snippet', CodeSnippet)


task :default do
  # copy static stuff
  `rm -rf public
  mkdir public
  cp -r site/* public
  rm -rf public/_*`

  layout = Liquid::Template.parse(open('site/_views/layout.liquid').read())
  
  # generate recipe pages
  recipe_header = open('site/_views/recipe_header.liquid').read()
  recipes = Dir['recipes/*/*/'].map do |dir|
    name = dir.split('/').last + '.html'
    puts dest = "public/#{name}"
    open(dest, 'w') do |out|
      Dir.chdir(dir) do
        meta = YAML.load(open('meta.yml').read())
        recipe = Liquid::Template.parse(recipe_header + open('recipe.md').read())
        markdown = recipe.render('meta' => meta)
        content = RDiscount.new(markdown).to_html
        out.write layout.render('meta' => meta, 'content' => content)
        { 'title' => meta['title'], 'href' => name }
      end
    end
  end.compact
  
  # generate index page
  puts dest = 'public/index.html'
  open(dest, 'w') do |out|
    index = Liquid::Template.parse(open('site/_views/index.liquid').read())
    out.write layout.render('content' => index.render('recipes' => recipes))
  end
end
