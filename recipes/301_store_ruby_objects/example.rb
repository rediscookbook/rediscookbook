### Example with ohm ###

#event.rb

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

#irb

    event = Event.create :name => "Ohm Worldwide Conference 2031"
    event.id
    # => 1

    # Find an event by id
    event == Event[1]
    # => true

    # Trying to find a non existent event
    Event[2]
    # => nil


### Example with remodel ###

#books.rb

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

#irb

	>> require 'books.rb'
	=> true
	>> book = Book.create :title => 'Moby Dick', :year => 1851
	=> #<Book(b:3) title: "Moby Dick", year: 1851>
	>> chapter = book.chapters.create :title => 'Ishmael'
	=> #<Chapter(c:4) title: "Ishmael">
	>> chapter.book
	=> #<Book(b:3) title: "Moby Dick", year: 1851>

