### Problem

You want to view your data just as in an relational datbase, such as the following examples in Oracle:
select * from all_objects;
describe table_a;


### Solution

Utilize Redis' KEYS (regex compatible) command to take a look at all your objects and the command TYPE to know what kind of structure the object has.

        $redis-cli
	# list all objects 
        127.0.0.1:6379> KEYS *
	# list all objects starting with hello
	127.0.0.1:6379> KEYS hello*
	1) "hello"
	2) "hello_bruce"
	# to see what kind of data structure a key holds
	127.0.0.1:6379> TYPE hello_bruce
	string

### Discussion

The use 

See *Storing Ruby Objects in Redis* for more examples of using unique ID's.

### See Also
http://redis.io/commands/keys
http://redis.io/commands/type
