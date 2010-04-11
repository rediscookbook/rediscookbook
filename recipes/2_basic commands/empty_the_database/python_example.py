"""
Empty the database - example
Language: Python
Client : redis-py
"""

#Instantiate the Redis object
r = redis.Redis()

#Delete all keys and values
r.flushdb()

