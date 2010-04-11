### Problem

You want to be able to:

* Install Redis on a Linux, OS X, or a similar Posix operating system
* Use a standardized layout for configurations and binary locations
* Have a /etc/{init.d,rc.d}/redis system control script when installing as root
* Install to one or more remote hosts
* Have the ability to install locally using *one* command

### Solution

Use [redis-installer](http://github.com/wayneeseguin/redis-installer/).

1. Installing on localhost:

First, download and/or clone the redis-installer: 

	git clone git://github.com/wayneeseguin/redis-installer/

Next, actually install Redis:

	bin/install-redis

2. Installing on localhost with **one** command

"I am not lazy, I am efficient!"

	bash < <(curl http://github.com/wayneeseguin/redis-installer/raw/master/bin/install-redis)

3. Installing on multiple remote hosts

First, download and/or clone the redis-installer from:

	git clone git://github.com/wayneeseguin/redis-installer/

Next, install Redis on one or more remote hosts

	bin/install-redis-on-hosts hostname1 [hostname2 [hostname3 ...]]

### Discussion

Note that installation and configuration is different based on whether you install as root or install as user. For root, it installs Redis to /usr/local/ and for a user it installs to ~/.redis/

Solution 2 simply downloads the Redis installer script, and feeds it directly into `bash` to execute the commands.

### See Also
