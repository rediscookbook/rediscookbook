r = redis.Redis()

r.set("place:100:name", "Spain")
r.get("place:100:name")
# > "Spain"

id = r.incr("name_ids")
r.set("person: %s:name" %id, "Donald Knuth")
r.get("person: %s:name" %id)
# > "Donald Knuth"


