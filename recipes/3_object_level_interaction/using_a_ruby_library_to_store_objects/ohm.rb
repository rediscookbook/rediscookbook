require 'ohm'

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
