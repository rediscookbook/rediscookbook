# GET/DEL - example
# Language: Ruby
# Client : redis-rb

require 'rubygems'
require 'redis'

r = Redis.new


puts r.set('TOTO', 1)
puts r.get('TOTO')

puts r.rename('TOTO', 'TOTO:TMP')
puts r.get('TOTO:TMP')
puts r.del('TOTO:TMP')

puts r.get('TOTO')

