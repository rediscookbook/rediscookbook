# Search usernames that begins with given phrase
#
# usernames: (username1, username2, ..)
# userscore:<username>: float
# user:obj: { id: int, username: string }

usernames_zset = "usernames"

def my_ord(c):
    return "%03d" % ord(c)

def get_score(s):
    return '0.' + ''.join(map(str, map(my_ord,s)))

def get_next_score(s):
    s_score = get_score(s)
    part0 = s_score[:4]
    c = s_score[4]
    next_c = str(int(c)+1)
    part1 = s_score[5:]
    return part0 + next_c + part1

def add_user(conn, username, score):
    # The User Object
    uid = conn.incr('user:idgen')
    conn.hset('user:obj:%d' % uid, 'id', username)
    # datastructures necessary to implement search
    conn.zadd(usernames_zset, username, score)

def add_test_data(conn):
    test_data = ('abc', 'ab', 'a', 'shekhar', 'shon', 'sh', 'zxcvbnmasdfghjklqwertyuiop0', 'zxcvbnmasdfghjklqwertyuiop00')

    for username in test_data:
        score = get_score(username)
        add_user(conn, username, score)

import redis
conn = redis.Redis()

add_test_data(conn)

# conn.zrange(usernames_zset, 0, -1) # Whole set
a_score = get_score('a')
b_score = get_next_score('a')

print 'Find all users starting with "a" -> INF'
print conn.zrangebyscore(usernames_zset, a_score, 'INF')
print 'Find all users starting with "a"'
print conn.zrangebyscore(usernames_zset, a_score, b_score)
print 'Find all users starting with "a" limit 2'
print conn.zrangebyscore(usernames_zset, a_score, 'INF', 0, 2)

