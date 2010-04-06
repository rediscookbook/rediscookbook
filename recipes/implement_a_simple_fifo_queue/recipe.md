#Implement a Simple FIFO Queue

Problem
-------

You want to use Redis to implement a simple abstract first-in, first-out
queue, with basic push and pop operations.

Solution
--------

Redis' built-in `List` datatype is a natural-born queue. To effectively
implement a simple queue, all you need to do is utilize a limited set 
of `List` operations. 

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

Redis comes with four basic list push and pop operations (RPUSH, LPUSH, 
LPOP, RPOP), as well as *blocking pop* operations. They are all O(1) 
operations, so the time complexity of the commands does not depend upon
 the length of the list. 

Implementing a simple queue atop the Redis commands is straight-forward
and is a good introduction to building thin Redis-powered abstractions. 

For example,  here's a Python queue that provides object-level 
interaction (and uses INCR to ensure a unique ID for each new queue): 

    r = redis.Redis()

    class Queue(object):
        """An abstract FIFO queue"""
        def __init__(self):
            local_id = r.incr("queue_space")
            id_name = "queue:%s" %(local_id)
            self.id_name = id_name
 
    def push(self, element):
        """Push an element to the tail of the queue""" 
            id_name = self.id_name
            push_element = redis.lpush(id_name, element)
 
    def pop(self):
        """Pop an element from the head of the queue"""
            id_name = self.id_name
            popped_element = redis.rpop(id_name)
            return popped_element
 

