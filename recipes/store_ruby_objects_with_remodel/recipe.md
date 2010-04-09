# How to Store Ruby Objects with Remodel

### Problem

You want to store some arbitrary Ruby objects in Redis.


### Solution

Use [remodel](http://github.com/tlossen/remodel), 
which provides a simple DSL for for describing persistent entities:

	require 'remodel'
	
	class Book < Remodel::Entity
	  has_many :chapters, :class => 'Chapter', :reverse => :book
	  property :title, :class => 'String'
	  property :year, :class => 'Integer'
	end

	class Chapter < Remodel::Entity
	  has_one :book, :class => Book, :reverse => :chapters
	  property :title, :class => String
	end

If you store the above as `books.rb` and have Redis running locally, 
then you can open a ruby shell and do:

	>> require 'books.rb'
	=> true
	>> book = Book.create :title => 'Moby Dick', :year => 1851
	=> #<Book(b:3) title: "Moby Dick", year: 1851>
	>> chapter = book.chapters.create :title => 'Ishmael'
	=> #<Chapter(c:4) title: "Ishmael">
	>> chapter.book
	=> #<Book(b:3) title: "Moby Dick", year: 1851>


### Discussion

There are different ways of storing ruby objects in Redis. 
Remodel, which describes itself as "a minimal object-redis-mapper",
uses a simple mapping strategy: all properties of an object are
serialized into a JSON hash, which is stored under a single key.
Associations are handled differently, though -- both ends of the
association are stored under separate keys. `has_many` uses a redis
list to store the keys of associated objects, `has_one` uses a redis
string to store the single associated key. This approach has the
advantage that associations can be modified without having to (de-)serialize
any objects.

A different mapping approach is implemented by [Ohm](http://github.com/soveran/ohm), 
another Ruby object-redis-mapper. Ohm stores each property under a separate key.
