### Problem

You want to use [remodel](http://github.com/tlossen/remodel) to persist Ruby objects.

### Solution

Remodel provides a simple DSL for describing persistent entities:

	require 'remodel'
	
	class Cookbook < Remodel::Entity
	  has_many :recipes, :class => 'Recipe', :reverse => :book
	  property :title, :class => String
	  property :author, :class => String
	end
	
	class Recipe < Remodel::Entity
	  has_one :book, :class => Cookbook, :reverse => :recipes
	  property :name, :class => String
	end

If you store the above as `cookbook.rb` and have Redis running locally, 
then you can open a Ruby shell and do:

	>> require 'cookbook.rb'
	=> true
	>> book = Cookbook.create :title => 'Python Cookbook', :author => 'Alex Martelli'
	=> #<Cookbook(c:1) title: "Python Cookbook", author: "Alex Martelli">
	>> recipe = book.recipes.create :name => 'Sorting a Dictionary'
	=> #<Recipe(r:4) name: "Sorting a Dictionary">
	>> recipe.book
	=> #<Cookbook(c:1) title: "Python Cookbook", author: "Alex Martelli">

### Discussion

Remodel, which describes itself as "a minimal object-redis-mapper",
uses a simple mapping strategy: all properties of an object are
serialized into a JSON hash, which is stored under a single key.

Associations are handled differently, though &mdash; both ends of the
association are stored under separate keys. `has_many` uses a Redis
list to store the keys of associated objects, `has_one` uses a Redis
string to store the single associated key. This approach has the
advantage that associations can be modified without having to (de-)serialize
any objects.
