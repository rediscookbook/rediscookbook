#Implement a Simple FIFO Queue

Problem
-------

You want to use Redis to implement a simple abstract first-in, first-out queue, with basic push and pop operations.

Solution
--------

Redis' built-in `List` datatype is a natural-born queue. To effectively implement a simple queue, all you need to do is utilize a limited set of `List` operations. 

	redis> LPUSH queue1 tom
	(integer) 1
	redis> LPUSH queue1 dick
	(integer) 2
	redis> LPUSH queue1 harry
	(integer) 3
	redis> RPOP queue1
	tom
	redis> RPOP queue1
	dick
	redis> RPOP queue1
	harry


	

Discussion
----------

