#Instantiate the Redis object
r = redis.Redis()
#Delete all keys and values
r.flushdb()

