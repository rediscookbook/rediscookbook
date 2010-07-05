### Problem
You want tags for your objects, and want to be able to search them.

### Solution
In this case, using books as an example, create one SET for each tag, and 
associate the given ids to the correct sets. Selecting a combination 
between tags is simple as using SINTER, SUNION and SDIFF. The same principle
can be used for document storage, taking care to use words or its stems 
as 'tags'

In redis-cli:

    SET book:1 {'title' : 'Diving into Python',
    'author': 'Mark Pilgrim'}
    SET book:2 { 'title' : 'Programing Erlang',
    'author': 'Joe Armstrong'}
    SET book:3 { 'title' : 'Programing in Haskell',
    'author': 'Graham Hutton'}

    SADD tag:python 1
    SADD tag:erlang 2
    SADD tag:haskell 3
    SADD tag:programming 1 2 3
    SADD tag computing 1 2 3
    SADD tag:distributedcomputing 2
    SADD tag:FP 2 3

Now, the searching/selecting part:

    a)  SINTER 'tag:erlang' 'tag:haskell'
        0 results

    b)  SINTER 'tag:programming' 'tag:computing'
        3 results: 1, 2, 3

    c)  SUNION 'tag:erlang' 'tag:haskell'
        2 results: 2 and 3

    d)  SDIFF 'tag:programming' 'tag:haskell'
        2 results: 1 and 2 (haskell is excluded)

### Discussion

SETs and ZSETs operations are building blocks for basic and advanced
combinations which yields more results per search.
 
* In (a), there is no book tagged erlang AND haskell. 
* In (b) is the same as searching for ALL BOOKS tagged programming and 
computing
* BOOKS that are tagged either erlang or haskell are found on (c)
* (d) excludes all books tagged haskell from the programming group.

For a document based storage and search, check meta code at 
<http://github.com/gleicon/docdb>. It may look overkill, but after some 
documents, the number of sets doesnt grow that much.
  
### See Also

* <http://www.slideshare.net/gleicon/redis-3025589>
* <http://docs.python.org/library/sets.html>
* <http://en.wikipedia.org/wiki/Stemming>
* <http://tartarus.org/~martin/PorterStemmer/>

