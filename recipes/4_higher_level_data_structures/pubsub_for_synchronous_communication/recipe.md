### Problem

You want Redis to serve as the backend for an application that needs chat
like communication (or arbitrary synchronous communication) between its
users.

### Solution

Use the Redis built-in commands `PUBLISH` and `SUBSCRIBE`. These commands
use the concept of channels. A client is able to PUBLISH messages on
any channel as well as `SUBSCRIBE` to any channel to receive messages.
Channels have a one-to-many relation. This means that a message that is
`PUBLISH`'ed against a channel is received by every subscriber.

When a client issues a `SUBSCRIBE` command, it cannot issue other commands
than `SUBSCRIBE` and `UNSUBSCRIBE` until it is no longer subscribed to any
channel. This means that it is important to think about how your
application handles Redis connections. The easiest approach is to create
a Redis connection for every user that issues one or more `SUBSCRIBE`
commands.

In the following example, `connectionA` and `connectionB` depict different
connections for different users.

    connectionA> SUBSCRIBE room:chatty
    ["subscribe", "room:chatty", 1]

    connectionB> PUBLISH room:chatty "Hello there!"
    (integer) 1

    connectionA> ...
    ["message", "room:chatty", "Hello there!"]

    connectionA> UNSUBSCRIBE room:chatty
    ["unsubscribe", "room:chatty", 0]

The `SUBSCRIBE` and `UNSUBSCRIBE` commands always return a three element array
containing the action that was just performed, the channel that was concerned
in the operation, and the number of remaining subscriptions after the operation.

**Note**: once a client has a subscription to a channel, you should always be ready
for incoming messages. It is therefore easiest to use an event-loop model for
the Redis connection pool.

### Discussion

When implementing `PUBLISH`/`SUBSCRIBE` in a web environment, the easiest
approach to use is to use [Web Sockets](http://en.wikipedia.org/wiki/Web_Sockets).
Using WebSockets, you are able to leverage the synchronous nature of
`PUBLISH`/`SUBSCRIBE` and immediately write incoming messages on the
subscribed channels to the user's specific Web Socket.

At the time of writing, the commands discussed in this recipe are new.
They're not available in a stable Redis release. Make sure to use the
development version of Redis until 2.0 is released.

### Variants

#### Persisting messages

In the scenario of a web chat, it is not unlikely you want to persist the
messages that were `PUBLISH`'ed. One way to implement this is to store
messages in a list. When this method is used, you can use `LRANGE` to retrieve
the last `N` messages that were `PUBLISH`'ed against the channel.

    MULTI
    LPUSH room:chatty:backlog (message)
    PUBLISH room:chatty (message)
    EXEC

However, if you need to do more complex tasks on the messages that were sent,
you could choose to use a sorted set. When the message timestamp is used
as the score, you can easily retrieve all messages that were sent in a
given time frame, using `ZRANGEBYSCORE`.

#### Big brother

Consider you need to have a way of monitoring all channels in your application.
One way to implement this, is to add a control channel that is used to
announce new channels being `SUBSCRIBE`'d to and unused channels being
`UNSUBSCRIBE`'d from. However, this method is costly and requires unnecessary
logic in your application. To solve this, you can use the `PSUBSCRIBE` command.
This command allows a client to subscribe to a pattern of channel identifiers.
To receive all messages in all chat rooms, the following command can be issued:

    PSUBSCRIBE room:*

Because every messages that travels through a channel includes the name of
the channel, the messages that are received using pattern-subscribe can be
easily identified.

### See Also

Check out **Atomically Pipeline Multiple Commands** to see how the order of messages
is preserved in persisting them by using `MULTI`/`EXEC`.

For a working example on publish/subscribe in Redis, see
[this Gist](http://gist.github.com/348262).
