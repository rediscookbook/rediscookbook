# How to Store Ruby Objects

### Problem

You want to store some arbitrary Ruby objects in Redis.

### Solution

As with any key-value database, you can use the key to simulate structure:

    >> redis.set "event:42:name", "Redis Meetup"
    => "OK"

    >> redis.get "event:42:name"
    => "Redis Meetup"

And the same example, but this time generating a unique ID first:

    >> id = redis.incr "event"
    => 1

    >> redis.set "event:#{id}:name", "Redis Meetup"
    => "OK"

    >> redis.get "event:#{id}:name"
    => "Redis Meetup"

Another approach is to serialize the data you want to store and decode it when you retrieve it:

    >> id = redis.incr "event"
    => 2

    >> redis.set "event:#{id}", {:name => "Redis Meetup"}.to_json
    => "OK"

    >> JSON.parse redis.get("event:#{id}")
    => {"name" => "Redis Meetup"}

Yet another approach, available in recent versions of Redis, is to use the new Hash datatype:

    >> id = redis.incr "event"
    => 3

    >> redis.hset "event:#{id}", "name", "Redis Meetup"
    => "OK"

    >> redis.hget "event:#{id}", "name"
    => "Redis Meetup"

As you can see, Redis is very flexible and lets you decide the best strategy for storing information.

There are some libraries that help you automate the creation of keys based on object attributes. Check them to learn how to use them:

* [DataMapper Adapter](http://github.com/whoahbot/dm-redis-adapter)
* [Redis Model](http://github.com/voloko/redis-model)
* [Redis Objects](http://github.com/nateware/redis-objects)
* [Remodel](http://github.com/tlossen/remodel)
* [Ohm](http://ohm.keyvalue.org)
