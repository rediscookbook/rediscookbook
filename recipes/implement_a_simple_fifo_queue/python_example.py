
#Redis object
r = redis.Redis()

#The simple queue class
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

#Push and pop operations

queue1 = Queue()

queue1.push('Hamlet')
queue1.push('Macbeth')
queue1.push('Romeo and Juliet')
queue1.pop()
queue1.pop()




