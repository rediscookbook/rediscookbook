### Problem

You want to atomically GET and then DELETE an object from Redis.

### Solution

in pseudocode:

	success = RENAME key key:tmp
	if success
	  value = GET key:tmp
	  DELETE key:tmp
	  return value
	end

using `redis-cli`:

	>> SET TOTO 1
	OK
	>> GET TOTO
	1
	>> RENAME TOTO TOTO:TMP
	OK
	>> GET TOTO:TMP
	1
	>> DEL TOTO:TMP
	(integer) 1
	
	>> GET TOTO
	(nil)
	>> RENAME TOTO TOTO:TMP
	(error) ERR no such key

### Discussion

This is a simple one, but makes good use of Redis' atomic features. The
RENAME function will succeed for first caller, subsequent callers will fail
because the key was already renamed. GET and DEL benefit from the RENAME
function in order to keep other clients from reading the object data between
operations.

This is potentially dangerous.

### Problems with the solution proposed above

If the execution is interrupted in line 2 (if success) or 3 (value = GET key:tmp) then that key stays renamed as key:tmp for good in the database.

### Real atomic solution

in pseudocode:

	MULTI
	value = GET key
	DELETE key
	EXEC	
	return value

using `redis-cli`:

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
	
### See Also

