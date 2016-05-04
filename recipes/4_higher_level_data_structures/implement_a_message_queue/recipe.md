### Problem
You want to use a simple Message Queue for your applications, with the whole message stored on Redis.

### Solution

For a queue named 'foo', we will create the MQ with the first message inserted:

    redis> incr FOO:UUID
    (integer) 1
    redis> set FOO:1 my_message
    OK
    redis> sadd QUEUESET FOO
    (integer) 1
    redis> LPUSH FOO:queue FOO:1
    (integer) 1
    redis> 

To get a message out of this MQ:

    redis> RPOP FOO:queue
    "FOO:1"

To list all MQs in the server:

redis> smembers QUEUESET
    1. "FOO"
    2. "BAR"

To read the next message from a MQ, without RPOPing it:
    
    redis> LINDEX FOO:queue -1
    "FOO:2"

### Discussion
The core of this solution is similar to "implement a fifo queue" recipe, except that you create a SET to hold all queues, and UUID generators for each queue. This was the solution I used at RestMQ.

Using a SET to hold all queues provide a control mechanism and index to disable or make a queue 'invisible'.

Reading instead of RPOP can be used to start a job scheduler, so you can only take a message from a queue later, when the job is finished.

Having a UUID generator for each queue ensures the uniqueness of each message.

The example below uses sinatra, but it's trivial to port to bottle and python (and any other DSL). The advantage is that different MQ using this algorithm can be used together sharing the same Redis server.


    require 'rubygems'
    require 'sinatra'
    require 'redis'
    require 'json'

    QUEUESET = 'QUEUESET'   # queue index
    UUID_SUFFIX = ':UUID'   # queue unique id
    QUEUE_SUFFIX = ':queue' # suffix to identify each queue's LIST

    reds = Redis.new

    get '/q' do
      b = reds.smembers QUEUESET
      throw :halt, [404, 'Not found (empty queueset)'] if b == nil
      b.map! do |q| q = '/q/'+q end
      b.to_json  
    end

    get '/q/*' do
      queue = params['splat'].to_s
      soft = params['soft'] # soft = true doesn't rpop values
      throw :halt, [404, 'Not found'] if queue == nil
      queue = queue + QUEUE_SUFFIX
      if soft != nil
        puts queue
        b = reds.lindex queue, -1
      else
        b = reds.rpop queue 
      end
      throw :halt, [404, 'Not found (empty queue)'] if b == nil
      v = reds.get b
      throw :halt, [200, "{'value':" + v + "'key':" + b + "}"] unless v == nil 
      'empty value'
    end

    post '/q/*' do
      queue = params['splat'].to_s
      value = params['value'].to_s
      throw :halt, [404, "Not found"] if queue == nil
      q1 = queue + QUEUE_SUFFIX
      uuid = reds.incr queue + UUID_SUFFIX 
      reds.sadd QUEUESET, q1
      lkey = queue + ':' + uuid.to_s
      reds.set lkey, value
      reds.lpush q1, lkey
      '{ok, '+lkey+'}'
    end

### See Also

http://github.com/gleicon/restmq
http://github.com/defunkt/resque

