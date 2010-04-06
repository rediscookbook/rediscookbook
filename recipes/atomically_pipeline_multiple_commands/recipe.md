# How to Atomically Pipeline Multiple Commands

### Problem

You want to execute several Redis commands with a single atomic command.

### Solution

Use the MULTI/EXEC command to create a queue of commands and execute them atomically.
Use the `MULTI` command to start the queue. Redis reponds with an `OK.` Then queue up
each command. Finally, use `EXEC` to execute the commands. Redis returns a multi-bulk
reply with each command's return value. In this basic example, we add three values to a 
list, increment (by 3) a key called 'country-count' and then ask for the range
of all the the values of the list.

	redis> MULTI
	OK
	redis> LPUSH country_list france 
	QUEUED
	redis> LPUSH country_list italy
	QUEUED
	redis> LPUSH country_list germany
	QUEUED
	redis> INCRBY country_count 3
	QUEUED
	redis> LRANGE country_list 0 -1
	QUEUED
	redis> EXEC
	1. (integer) 1
	2. (integer) 2
	3. (integer) 3
	4. (integer) 3
	5. 
	 1. germany
	 2. italy
	 3. france
	 

### Discussion

MULTI/EXEC, which was added in Redis 2.0, is an extremely important component of Redis and merits
a good deal of discussion.
