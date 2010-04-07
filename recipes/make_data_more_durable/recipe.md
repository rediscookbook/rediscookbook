# Make Data in Redis More Durable With The Append-Only File

### Problem

You want to increase the durability of your data in Redis.

### Solution

Use Redis' built-in *append-only file* (AOF). 

Edit the Redis configuration file to include the line:
	appendonly yes

Redis will now add every command to the AOF. If the server should crash, you will be able to 
rebuild state from this file. It works in a very similar fashion to the log files common in 
other databases, such as MySQL's binlog.

### Discussion


