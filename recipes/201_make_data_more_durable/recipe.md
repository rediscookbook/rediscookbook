### Problem

You want to increase the durability of your data in Redis.

### Solution

Use Redis' built-in *append-only file* (AOF). 

Edit the Redis configuration file `redis.conf` to include the line:
	appendonly yes

Redis will now add every command to the AOF. If the server should crash, you will be able to 
rebuild state from this file. It works in a very similar fashion to the log files common in 
other databases, such as MySQL's binlog.

### Discussion

The AOF itself is configurable. There are three different options, each with their own particular
tradeoff between durability and speed. These configurations can be set in `redis.conf`.

The three options are to force a sync every command, sync every second, or never force a sync (that is, leave the process up to the operating system). Redis' default is the sync on every command; however, this will be quite slow. The second option is usually a fair trade-off between safety and speed.





