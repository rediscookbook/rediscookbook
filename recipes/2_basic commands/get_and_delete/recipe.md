### Problem

You want to atomically GET and then DELETE an object from Redis.

### Solution

success = RENAME key key:tmp

if success

  value = GET key:tmp

  DELETE key:tmp

  return value

end


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
        >> RENAME TOTO TOTO:TMP
        (error) ERR no such key

### Discussion

This is a simple one, but makes good use of Redis' atomic features. The RENAME function will succeed for first caller, subsequent callers will fail because the key was already renamed. GET and DEL benefit from the RENAME function in order to keep other clients from reading the object data between operations.

### See Also

