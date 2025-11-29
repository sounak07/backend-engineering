## Facebook' Memcache


##### Why Memcache ?

Facebook's popularity forced it scale at a massive level to support 
- Almost Real-time communication
- Scale at billion users for sec across multiple regions
- Scale to handle many many users shared across the world.
- Push the most popular content into the users newsfeed.
##### What is memcache? 
Memcache is a in memory key value store with certain set of operations like Set, get, delete. Its a forked and extended version of a single machine key value store which is made into a distributed cache. 

***Query Cache***
This is to reduce load on the database. 
Facebook uses Memcache as a *Demand filled look aside cache* , it means data goes it cache only if requested i.e., demand filled and its first checks the cache before checking the database. 

![alt text](/resources/Screenshot%202024-03-08%20at%2011.38.33%20PM.png)

The write flow is a bit different here , if an update happens it gets deleted from Memcache but not added, because its a demand filled cache. 

***Generic Cache***
Memcache being used as a key-value store for storing various data like the ML extracted results etc.

##### The overall Architecture

![alt text](/resources/Screenshot%202024-03-08%20at%2011.52.23%20PM.png)


Storage cluster here stores the *source-of-truth* , the database.
There are certain challenges that needs to be solved in this architecture.
- Latency, load or failures within the clusters.
- Replication 
- Consistency across the primary and secondary regions.

#### Intra-cluster Challenges

Dealing issues with cluster which contains webserver and memcache server. 

**Reducing Latency**
A single get request can start 100s of fetch request from memcache. So webserver must communicate with many memcache servers with a short period. So this could introduce latency.
![alt text](/resources/Screenshot%202024-03-09%20at%2012.15.42%20AM.png)

*Parallel fetching and Batching* 
So as we can see the webserver uses something called DAG (Directed Acyclic graph) to determine where there can be batch or parallel fetching can be done. 

*UDP for reads and TCP for writes*
UDP since its connectionless and sends data as per an interface and introduces less latency. There can be data packets drop here because UDP does not guarantees data delivery or retry mechanism but those scenarios can be treated as cache miss. 

TCP for writes as its more reliable and removes the need for retry as TCP handles retransmission on its own which is not the case for UDP. This is important for update and delete.

##### Reducing Load

The primary Goal of this Memcache is to avoid database reads as they are expensive operations. So the cache needs to be properly updated in order achieve consistency of data.

There are two major challenges to this -
- Stale sets
- Thundering Herd problem

*Stale sets*  occurs when a invalid data is updated into the cache and its doesn't get validated.
*Thundering Herd problem* where a single cache miss could cause concurrent requests occurs on the server by many clients for the same key.
This problem is usually solved by something called **leasing**.

Suppose there is a cache miss , so its the client's responsibility to update the cache. But suppose the same cache miss happens for another client, there would be a client trying to update the cache again. 

Leasing in a technique where when a client tries to update , it is issued a 64 bit token that is associated with that key. So when clients try to update the cache, there are issued a token to set the value with, the client with most latest token is allowed to set the value to the cache because latest token means latest read from db. 
This way cases of *stale sets* are prevented as this way the old value will not be updated into the cache.  

Memcache regulates the rate at which Leasing tokens are issued , so whenever multiple clients try to update the cache memcache sends a special request that an update is already telling the clients that an update is going to happen soon so wait for a bit. So whenever that client requests again they most probably find the value.

As per their measurements, the leasing approach alone helped reduce peak DB query rates from **17K/seconds** to **1.3K/seconds**.

##### Handling Failures

When clients fail to reach memcache, backend gets overloaded which might cause outages. For widespread outages , facebook diverts the data to other clusters, but for small outages they use a self redemption technique, which takes time to kick in. 
This is where the gutter machines come in. 
When the clients do not receive a response from the memcache cluster even a cache miss , they assume that the cluster has failed, so they divert the request to gutter machines. On cache miss, client fetch the data from db and update the gutter machines.
The gutter cache gets expired after a certain time so no need to invalidate.

![alt text](/resources/Screenshot%202024-03-10%20at%2012.05.39%20AM.png)

There might be some stale sets since gutter does not have load mechanism like memcache but thats a trade off facebook is ok with. 

You might wonder why Facebook uses Gutter machines instead of just redistributing keys among the remaining servers when some servers fail.

The reason is that redistributing keys can be risky. Imagine if one key is really popular and gets accessed a lot. If that key ends up on one server, that server could get overwhelmed with requests. This could cause a chain reaction, leading to more servers getting overloaded and potentially crashing. So, instead of risking this cascade effect, Facebook uses Gutter machines to handle these situations more safely.

#### Intra-Region Failures

The biggest intra-region challenge Facebook had to solve is around handling **invalidations** across multiple frontend clusters.
Users may connect to different clusters in different times creating duplicates in memcache servers.

**How do you invalidate this data across all the clusters of a region in case of any update?**
![alt text](/resources/Screenshot%202024-03-10%20at%2012.44.14%20AM.png)

##### Cluster Level

 A webserver that updated a key is responsible for invalidating it within its own cluster. It usually maintains keys that they are responsible for . Using this data and few other things they usually try invalidate duplicates.

##### Region level

The region level duplicates are invalidated not by webservers but by the storage cluster. 
A daemon called mcsqueal usually runs to check the commits logs to identify the deletes and the batches these deletes in fewer packets and then sends them to dedicated servers running mcrouter in each cluster which then unpacks and sends the data to the correct memcache servers. 


![alt text](/resources/Screenshot%202024-03-10%20at%2012.26.35%20AM.png)


#### Across-Region Challenges 

Placing clusters at different regions have many advantages which includes low latency for being closer to the user, diversity and lower probability of failures due to natural disasters and incentives and lower cost at new regions.

One of the main challenges across regions is to maintain consistency about the databases and memcache. In Facebook's setup, there is a primary database in one region while the secondary regions are only read replicas. The read replicas are kept updated with various replication techniques. 
But there could be some replication lag involved in here. There are mainly two major challenges to this 

##### Writes from Primary region 

Any writes from the primary region needs to be propagated to all the secondary regions and while doing so memcache data needs to be invalidated. 
But if the invalidations happen before the replicas are updated, there could be a race condition.

Suppose the cache invalidation happens before cache update, there will be a cache miss , it will fetch data from db and update the cache , later the data gets updated by replication , so we now ended up with stale data.

To avoid this , facebook assigns this task to storage clusters. The storage cluster within the region with the most updated data has the responsibility to invalidate the cache with the same macqueal pipeline discussed above. 

##### Writes from the Replica Region 

When writes come into a secondary region, the writes are directed to primary region while reads are served from secondary region. 
The newly updated data in the primary region needs to be propagated to all the secondary regions. 
But if there is a read request to the secondary region before replication gets completed, it will get a stale set from the cache. 
Facebook solved this by using something called **remote marker**.

A remote marker indicates that the data in the cache might be invalid so the request should be redirected to the primary region. 

So whenever a write request comes to the secondary server for say key *k* , it sets a remote marker R and the write request is made to the primary region. Finally that key is deleted from secondary memcache server.
Whenever a read request comes to the secondary server, it first checks the cache then if not found it checks if the remote marker, if found it directs itself to the primary region for read.  

There is some latency while first needing to check the memcache and checking the remote marker to direct itself, but thats a trade-off facebook was ok with. 

#### Single server Optimizations

Facebook has to also introduce optimizations to the single memcache server to enhance its performance. Some of those include -

- Automatic expansion of hash maps to avoid lookups going to O(n).**
- Making server multi threaded
- Assigning a different UDP port to all the threads to avoid contention. (fight to get the port)
- Optimized memory management through adaption slab allocator.


The key takeways from this read is what are the challenges we face in cache management and how we can overcome those to scale it. 

** In hash maps each key is hashed to determine the index it should be stored. The hash function converts the key to a integer which is used to determine the key it(key-value) should be stored in, but as the map increases the collision of hash indexes might happen. So it is expanded automatically to maintain the performance.
The hash key/index doesn't refer to the key of the map set by user. 

When multiple key-values are stored in a single hash key , they are stored as chains so it takes O(n) time to recover it.


[Reference](https://newsletter.systemdesigncodex.com/p/facebook-memcache-breakdown)