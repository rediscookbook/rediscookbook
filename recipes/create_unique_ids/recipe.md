### Problem

You want to atomically provide a unique ID for an arbitrary object.

### Solution

Utilize Redis' built-in atomic INCR function.

	$redis-cli INCR <an_object_name>
	(interger) 1

	$redis-cli INCR <another_object_name>
	(interger) 2

	$redis-cli GET <an_object_name>
	1
		
	$redis-cli GET <another_object_name>
	2
	
### Discussion

The use of INCR to provide unique ID's is one of the core concepts in Redis. It is often used in the 'primary key' style, replacing the same functionality used in relational databases.

See *Storing Ruby Objects in Redis* for more examples of using unique ID's.
