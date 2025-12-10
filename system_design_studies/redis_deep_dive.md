## Redis Deep Dive

- Redis is single threaded. So its easier to use and implement without having to worry about concurrency.
- Redis is In-memory
- Redis can store any type of Data structure; str, list, bloom filters.

##### Commands

Redis CLI supports a bunch of commands

```
SET foo 1
GET foo     # Returns 1
INCR foo    # Returns 2
XADD mystream * name Sara surname OConnor # Adds an item to a stream
```

##### Infrastructure

Redis can run as a single node with a replica or as a cluster.
Even they clusters can have their replicas reading from main.

![alt text](https://raw.githubusercontent.com/sounak07/backend-engineering/main/resources/Screenshot%202025-12-10%20at%2011.37.26%20PM.png)

When ran as a cluster, Redis maintains a set of hash slots. A key is hashed and based on the hashed slot a key is assigned a cluster. These clusters do maintain a contact in between them using gossip protocols incase a wrong cluster was chosen but since redis optimises for speed the goal to reach the correct cluster in first go.

Redis sharding works via keys(hypothetically),incorrect choice of keys could lead to hot keys and a cluster being overloaded so choosing the right key in the way to scale.

- One way to to avoid hot keys is to append a random number so as to avoid putting the key in the one cluster and storing the same data in multiple clusters.
- Another way could be adding inmemory cache
- One way could be to add more read replicas of clusters and scale dynamically

##### Redis Use cases

**Distributed cache**
Most common use case is having it in between db and service, this allows faster data retrival and overloading database.

Expiration in redis is important to maintain a manageable amount of data. It can be set using TTL.

**Rate Limiter**

Redis atomic INCR command can be used to count the number of times a client making a request in a distributed manner for all the servers that are running.
I can also set for how long the counter value remain alive using EXPIRE command.

So say a user can make 5 req in 60 secs
So INCR to upto 5 in 60 secs in the limit of this system.

**Event Sourcing**

![alt text](https://raw.githubusercontent.com/sounak07/backend-engineering/main/resources/Screenshot%202025-12-11%20at%2012.08.14%20AM.png)

Redis streams are append only log files like kafka topics. Events can be added into the streams via commands like XADD and XCLAIM for storing the last claimed item.
At some point if the redis fails the cluster keeps track of the last processed item similar to offsets in kafka, starts processing them once back up.

**Leaderboard**

Redis's sorted sets can maintain an ordered set which can be queried in log time. This is something SQL will struggle to acheive. Redis's high write throughput and low latency makes it an ideal candidate.

**Proximity Search**

Redis supports geospatial indexing natively using `GEOADD` and `GEOSEARCH` command.

![alt text](https://raw.githubusercontent.com/sounak07/backend-engineering/main/resources/Screenshot%202025-12-11%20at%2012.27.56%20AM.png)

We can see from the example how it managed to search all the stations of bikerentals with a LATLONG range and Byradius.

This can be done in O(m)+O(log(n)). m and n because redis uses geohashing to index the data. These geohashes allow to grab candidates within grid-bounding boxes. But these boxes are squares and imprecise so a second pass makes the search more accurate.

**Distributed Lock**

Locking is a crucial concept in distributed systems where we might need to acquire a lock on some updates in order to maintain consistency. Usually databases offer native locks but this is a use case which can be useful in places where there is none.

How it works is using INCR with some indicator key
`INCR KEY` -> if it returns 1 , we may proceed since we acquired a lock.
`INCR KEY` -> If it returns > 1, we wait

We delete the key with `DEL`

**Pub/Sub**

![alt text](https://raw.githubusercontent.com/sounak07/backend-engineering/main/resources/Screenshot%202025-12-11%20at%2012.50.14%20AM.png)

A chat application is a example for this where we decouple the producers from consumers and introduce a redis Pub/Sub where the Redis knows the location of servers and any data publish from one server can reach the desired server if they are subscribed to redis.
Say server A sends a message for server C, Redis will act as a registry and deliver the message. Something similar can be achieved by consistent hashed ring but its a bit harder.
Redis Pub/Sub is atmost single delivery. Its very fast though.

#### References

[Redis Deep Dive(Hello Interview)](https://www.youtube.com/watch?v=fmT5nlEkl3U&)
