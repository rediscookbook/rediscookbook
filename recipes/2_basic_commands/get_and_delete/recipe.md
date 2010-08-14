### Problem

You want to atomically GET and then DELETE an object from Redis.

### Solution

Make use of Redis' built-in atomic functions, and MULTI-EXEC functionalty.

One approach to the problem might go something like this. In pseudo-code:

	success = RENAME key key:tmp
	if success
	  value = GET key:tmp
	  DELETE key:tmp
	  return value
	end

This is a simple one, but makes good use of Redis' atomic features. The
RENAME function will succeed for first caller, subsequent callers will fail
because the key was already renamed. GET and DEL benefit from the RENAME
function in order to keep other clients from reading the object data between
operations.

However, there is an potential problem lurking here. If the execution is 
interrupted on line 2  (if success) or line 3 (value = GET key:tmp), then 
that key stays renamed as `key:tmp` for good in the database.

Using Redis' MULTI-EXEC function provides a solution. 

First, in pseudocode:

	MULTI
	value = GET key
	DELETE key
	EXEC	
	return value

And using `redis-cli`:

	redis> SET TOTO 1
	OK
	redis> GET TOTO
	1
	redis> MULTI
	OK
	redis> GET TOTO
	QUEUED
	redis> DEL TOTO
	QUEUED
	redis> EXEC
	1. 1
	2. (integer) 1
	redis> GET TOTO
	(nil)


### Discussion

	
### See Also

**Atomically Pipeline Multiple Commands** for more information about MULTI/EXEC.

