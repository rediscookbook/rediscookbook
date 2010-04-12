### Problem

You want to use Redis to implement a social graph for users in
some kind of application, with one and two directional
relationships available (following and friendship).

### Solution

Use the built-in set functionality of Redis to construct `follow`,
`follower`, and `blocked` lists keyed to each user's unique ID. In
raw redis it looks something like this:

    redis> SADD user:1:follows 2
    (integer) 1
    redis> SADD user:2:followers 1
    (integer) 1
    redis> SADD user:3:follows 1
    (integer) 1
    redis> SADD user:1:followers 3
    (integer) 1
    redis> SADD user:1:follows 3
    (integer) 1
    redis> SADD user:3:followers 1
    (integer) 1
    redis> SINTER user:1:follows user:1:followers
    1. 3
    
### Discussion

Redis comes with the ability to construct "sets", which are
collections of unique values assigned to a key. By creating both a
"follows" and "followers" list for a given user, we are able to
quickly and easily pull that information as well as calculate
their "friendships" using a simple set intersection.

Implementing such a system in Ruby looks something like this:

{% code_snippet social_graph.rb %}