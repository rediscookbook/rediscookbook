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

# slugify method for strings
class String
  def slugify
    slug = self.downcase.gsub(/'/, '').gsub(/[^a-z0-9]+/, '_')
    slug = slug.chop! if slug =~ /_$/ 
    return slug
  end
end

# custom liquid filter
module SlugifyFilter
  def slugify(input)
    input.slugify
  end
end

Liquid::Template.register_filter(SlugifyFilter)

# default task
task :default do
  # copy static stuff
  `rm -rf public
  mkdir -p public/tag
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
        { 'title' => meta['title'], 'href' => name, 'tags' => meta['tags'] }
      end
    end
  end.compact

  # generate tag pages
  tags_dict = Hash.new
  recipes.each do |recipe|
    recipe['tags'].each do |tag|
      if not tags_dict.keys.include? tag
        tags_dict[tag] = Array.new
      end
      tags_dict[tag] << recipe
    end
  end

  tags_dict.keys.each do |tag|
    puts dest = "public/tag/#{tag.slugify}.html"
    recipes_for_tag = tags_dict[tag]
    open(dest, 'w') do |out|
      tag_page = Liquid::Template.parse(open('site/_views/tag.liquid').read())
      out.write layout.render('content' => tag_page.render(
        'tag' => tag, 'recipes' => recipes_for_tag))
    end
  end
  
  # generate index page
  puts dest = 'public/index.html'
  open(dest, 'w') do |out|
    index = Liquid::Template.parse(open('site/_views/index.liquid').read())
    out.write layout.render('content' => index.render('recipes' => recipes))
  end
end
