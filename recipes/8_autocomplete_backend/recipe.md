### Problem

You want to implement search against user objects stored in redis using Python. Something like querying for all user ids whose username begins with "an".

### Solution

Here we have user objects stored in as hashes with "user:obj:" as prefix.

For example

    user:obj:3955 {id: 3955, username: 'John', ..}

We need some extra data structures to support our search i.e. (search user objects where username begins with given phrase. So search for `jo` should match John, Joe and so on. We will use sorted sets of all usernames and will assign every element a score.
This score is a float and helps us in finding the matching words.

Some scores for eg.
    
    a -> 0.097
    ab -> 0.097098
    ac -> 0.097099
    bc -> 0.098099

So for above four string if we find strings that has score that is => 0.097 and < 0.098, we find all strings that begins with 'a'


{% code_snippet search.py %}

### Discussion

This to demonstrate simple redis pattern and using it in Python.

### See Also
 - [ZrangebyscoreCommand] http://code.google.com/p/redis/wiki/ZrangebyscoreCommand
There are already some good writeups on related topics.
 - [playnicely] http://playnice.ly/blog/2010/05/24/redis-multi-field-searching-and-filtering/
 - [autocomplete] http://antirez.com/post/autocomplete-with-redis.html
