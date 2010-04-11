"""
GET/DEL - example
Language: Python
Client : redis-py
"""
import redis

r = redis.Redis()

print r.set('TOTO', 1)
print r.get('TOTO')

print r.rename('TOTO', 'TOTO:TMP')
print r.get('TOTO:TMP')
print r.delete('TOTO:TMP')

print r.get('TOTO')

