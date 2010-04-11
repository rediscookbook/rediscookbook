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
