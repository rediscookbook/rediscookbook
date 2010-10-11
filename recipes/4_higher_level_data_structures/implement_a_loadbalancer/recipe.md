### Problem
You want a load balancer to choose between different servers and that can provide the best candidate for a given operation.
### Solution
Scored Sets (ZSets) already provides this abstraction. You might update the scores with your own metric and always select the better ranked candidate.

For a replica distribution cluster, separated in two server rows (lets say odd and even servers):

    redis> zadd odd_loadbalancer 10 server1
    (integer) 1
    redis> zadd odd_loadbalancer 20 server3
    (integer) 1
    redis> zadd odd_loadbalancer 1 server5
    (integer) 1
    redis> zadd odd_loadbalancer 5 server7
    (integer) 1
    redis> zadd even_loadbalancer 5 server2
    (integer) 1
    redis> zadd even_loadbalancer 10 server4
    (integer) 1
    redis> zadd even_loadbalancer 1 server6
    (integer) 1
    redis> zadd even_loadbalancer 20 server8
    (integer) 1

Selecting servers with score '1' (meaning that 1 is better for us, or the right server):

    redis> zrangebyscore odd_loadbalancer 1 1
    1. "server5"
    redis> zrangebyscore even_loadbalancer 1 1
    1. "server6"

So, using intersection and union we can get interesting results for a replica based load balancer (assuming that I have to store 'things' in at least two servers in different networks, racks, places, etc):

    redis> zunionstore dst_servers 2 odd_loadbalancer even_loadbalancer
    (integer) 8

    redis> zrangebyscore dst_servers 1 1
    1. "server5"
    2. "server6"
    redis> zrangebyscore dst_servers 3 3
    (empty list or set)
    redis> zrangebyscore dst_servers 5 5
    1. "server2"
    2. "server7"


### Discussion

The example above deals with two servers cluster that have to be balanced. The scores must be constantly updated so the result of any searches still relevant.

Lets say that server2 had its score updated to 50.

    redis> zadd even_loadbalancer 50 server2
    (integer) 0
    redis> zunionstore dst_servers 2 odd_loadbalancer even_loadbalancer
    (integer) 8
    redis> zrangebyscore dst_servers 5 5
    1. "server7"
    redis> zrangebyscore dst_servers 1 1 
    1. "server5"
    2. "server6"

    redis> zrangebyscore dst_servers 10 10
    1. "server1"
    2. "server4"


There are no pairs ate score 5 anymore, so zunionstore must be a little less restrictive to offer other ranges to be looked at. In this case, the scores 1 and 10 are a complete replica pair.


### See Also

Ezra's Redis presentation:
http://www.slideshare.net/ezmobius/redis-remote-dictionary-server

