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

If necessary, the DISCARD command can be used to clear the MULTI queue and exit the queue.

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

MULTI/EXEC, which was added in Redis 2.0, is an extremely important component of 
Redis and merits a good deal of discussion. It is important to know what it 
does -- and what it does not do.

M/E is 'atomic' in the sense that, while a queue is being executed, no other clients
will be served by the Redis server -- the queue is treated as a single operation. This
is important for data integrity.

The M/E process is designed to prevent syntax errors during execution by immediately
reporting syntax errors whenever a command is added to the queue. For example:

	redis> MULTI
	OK
	redis> LPUSH country_list italy
	QUEUED
	redis> LPUSH country_list italy germany
	Wrong number of arguments for 'lpush'


Now, M/E does *not* provide complete 'transactions' -- at least not in the ordinary
sense -- since it does not include 'rollback' functionality. 

Consider the following situation. You create a relatively large M/E queue (say, 
with 200 commands) and run EXEC. Before all the queued commands are executed, 
the server crashes, or perhaps it runs out of memory -- let's say that happens
at command #148. The first 148 commands are indeed executed, but the rest are not. 
Indeed, M/E is only an 'all or nothing' oepration *before* the EXEC command is run
(that is, during queueing) -- not during the execution. 

Redis does provide an intersting  way to deal with issue: the familiar Append-Only 
File. In the upcoming version of Redis, the commands in the queue are only written
to the AOF upon successful completion of the EXEC command. So if your server crashes
mid-EXEC, you can rebuild state according to the previous, pre-EXEC state. 



