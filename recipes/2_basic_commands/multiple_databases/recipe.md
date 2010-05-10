### Problem

You want to keep different kinds of data &mdash; belonging to different
applications, for example &mdash; separate from each other, but store them
all in the same Redis instance.


### Solution

Use different Redis databases for different kinds of data.
In Redis, databases are identified by an integer index, not by a database name.
By default, a client is connected to database 0.
With the `SELECT` command you can switch to a different database:

	redis> select 3
	OK
	
All subsequent commands will then use database 3, until you issue another `SELECT`.


### Discussion

Each Redis database has its own keyspace. 
By using different databases for your 'staging' and 'production' data,
for example, you don't have to worry about key clashes between the two.

There is also a command to drop all the data in a single database:

	redis> flushdb
	OK

This comes in very handy if you want to reset your 'staging' database.

If you want to get rid of all the data in a Redis instance, you can use
`FLUSHALL` instead. But be careful, there is no security check, and this
command is guaranteed to never fail.

The number of databases which is available can be configured in `redis.conf` &mdash;
by default, it is set to 16. Simply set it to a higher number if you need
more:

	databases 42

Unfortunately, Redis does not provide a way to associate names with the
different databases, so you will have to keep track of what data goes where
yourself.


### See Also


