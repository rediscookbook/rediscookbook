### Problem

You want to atomically provide a unique ID for an arbitrary object.

### Solution

Utilize Redis' built-in atomic INCR function.

	$redis-cli INCR <next_object_id>
	(integer) 1

    $redis-cli INCR <next_object_id>
    (integer) 2

	$redis-cli INCR <another_next_object_id>
	(integer) 1

	$redis-cli GET <next_object_id>
	2
		
	$redis-cli GET <another_next_object_id>
	1
	
### Discussion

The use of INCR to provide unique ID's is one of the core concepts in Redis. It is often used in the 'primary key' style, replacing the same functionality used in relational databases.

See *Storing Ruby Objects in Redis* for more examples of using unique ID's.

### See Also
