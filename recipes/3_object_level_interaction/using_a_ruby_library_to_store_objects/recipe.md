### Problem

You want to use an open source library to persist Ruby objects.

### Solution

Explore your options and pick one! There exist several libraries to store and persist objects in Ruby. 
In the following recipe, we'll use [Ohm](http://github.com/soveran/ohm) and [remodel](http://github.com/tlossen/remodel) as examples, but the reader should note that there are several good libraries that can be used for this purpose. 
[Please add more library examples with other libraries.]

A general abstraction strategy is to map objects without complicated schema definitions,
and instead use a very simple domain-specific language to achieve similar results.

Consider the following example in Ohm. Here, we'll model three arbitrary objects (an Event, a
Venue, and a Person), and provide validations for the Event.

	class Event < Ohm::Model
  	  attribute :name
  	  reference :venue, Venue
  	  set :participants, Person
  	  counter :votes

 	  index :name

   	  def validate
   	    assert_present :name
	  end
	end

	class Venue < Ohm::Model
  	  attribute :name
  	  collection :events, Event
	end

	class Person < Ohm::Model
 	 attribute :name
	end
 
The Ruby libraries also employ a simple style to model associations. Here is an example of how to create a 
familiar 'has_many' relationship, using remodel.

	require 'remodel'
	
	class Cookbook < remodel::Entity
	  has_many :recipes, :class => 'Recipe', :reverse => :book
	  property :title, :class => String
	  property :author, :class => String
	end
	
	class Recipe < remodel::Entity
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

An important reason to use an existing library to persist objects is the power of 
built-in *assertions,* or validations. Ohm, for example, includes assertions that ensure
a field matches a certain format, or that the the field is numeric. Regular expressions
can be used for the `format` validation:

	assert_format :username, /^\w+$/

There are various strategies for storing object propoerties. For example, in remodel, 
all properties of an object are serialized into a JSON hash, which is stored under a
single key. Associations are handled differently, though &mdash; both ends of the
association are stored under separate keys. `has_many` uses a Redis
list to store the keys of associated objects, `has_one` uses a Redis
string to store the single associated key. 

### See Also

