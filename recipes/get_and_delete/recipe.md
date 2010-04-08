#Atomically GET and DELETE data from Redis

### Problem

You want to atomically GET and then DELETE an object from Redis.

### Solution

new_key = RENAME key key:tmp

value = GET key:tmp

DELETE key:tmp

return value


        SET TOTO 1
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


	
### Discussion

This is a simple one, but makes good use of Redis' atomic features. GET and DEL benefit from the RENAME function in order to keep other clients from reading the object data between operations.

