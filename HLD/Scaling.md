
## Writes

[Scaling Writes](https://www.hellointerview.com/learn/system-design/patterns/scaling-writes)

During high throughput times, scaling the stateless servers becomes quite easy, just add a bunch of new servers, but when it comes to database, that could become a bottleneck.  There many ways to go about it.

**Vertical Scaling**
One choice if the math permits could be just vertical scaling or adding more hardware to it. Going towards sharding is not always the right choice immediately. 

**Database choice**
- Cassandra is a write heavy database because its an append only op but trade off is slow reads, which is the opposite of how postgres operates.
- Postgres handles reads very fast but can be slow to handle writes due to creation of indexes in the form of rebalancing the B-tree

**Horizontal Scaling**

- Picking sharding is important to avoid hot shards. We want to data to be spread out.
- Vertical partitioning is another to split the db with columns.

During surges in traffic, throttling using a queue is an option. But the request becomes async now and u need to think of an architecture when failures are handled. 
Now even queues are not always enough, if we write to queue faster than workers can consume, it would overflow. So we load shed, drop messages basically or apply backpressure. Lets say we drop some of the drivers locations updates, thats fine because we will get new ones soon. 


**Batching Writes**

- Batching at the application level during writes, but downside is if it crashes, its a problem unless its stored in queue.
- Intermediate Processing - Lets say we are counting likes, instead of updating it everytime in the database, we aggregate the counts lets say in redis and then flush them into disk after the count increased to certain no, this way we are able to quickly show lives to the user and the likes are eventually consistent for others. 
- Hierarchical sharding where we add Broadcast nodes on the reads assigning users using consistent hashing and then fan out the changes through them
  Similarly for writes we add processors nodes processing incoming data in batches and write. We can hash the comment id or some other identifier to assign  a node during write

![Screenshot_2026-07-24_at_8.22.23_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2026-07-24_at_8.22.23_PM.png)


**Adding more shards**

Increasing the no of shards without downtime is a challenge we often stumble upon. This can be solved by dual writes and syncing historical data.

**Hot shards**

Getting a lot of traffic on a shard due to a viral post likes could lead to hot shards. 
So there are two ways here - 

- Always split the shard in fixed no of k shards. This increasing the shards and keep unused spaces.
- Another way is to dynamically break the hot key into sub keys. But the reader needs to agree on how to read different keys based on how they are split



## Reads

[Scaling reads](https://www.hellointerview.com/learn/system-design/patterns/scaling-reads)

- **Adding indexing** - The first things to do is usually add the missing indexes for missing paths. Modern dbs handle databases really well, so while overindexing could be a problem but under indexing is a much major one. 
- **Vertical scaling** - Pump more hardware, but you can do so much.
- **Denormalisation** - General advise is to normalise data (different tables for different types of data) to avoid duplicates, heavy reads could be a problem here. During reads we need to join the tables, so denormalisation and merging them all into a single table could make the reads faster but the tradeoff is lots of duplicates data and consistency overhead as u need to update every row now.
- **Read replicas** - Leader and followers , we write to leader, sync to followers and serve reads
- **Sharding** - [Database Internals#Sharding in databases](./Database_Internals#Sharding_in_databases.md)
- Caching and CDN - Modern CDNs can also cache dynamic content. Basically CDN reduces latency by caching near the geolocation of user.

**Deep Dives**

- How do i scale huge no of requests coming in ?
  If data is skew(a subset of database), cache else use read replicas
- How do handle Hot key problem in cache? 
	- You coalaise(combine) requests for the same key and make a single request to cache to get the value and then return the value to everyone. 
	  - Cash key fan-out - If the above is not enough, Replicate cache clusters into multiple instances, server can randomly call any instance for answer, trade off is more memory, updates are slow due to multiple places to write. 
- How do you handle cache invalidation when data updates need to be immediately visible?
	- Most system accepts eventual consistency but some might not
	- One way could be to invalidate the cache when we write new data. We write -> we delete cache -> Nxt reads from db -> adds the cache. 
	- But lets say we have a situation where while we were doing the above, some problems come in - 
		-  Which caches do you delete from—application cache, CDN, browser?
		- What if an invalidation request fails?
		- What if a request comes in right after you delete the old value but before the new value is written in db or it reads from replica? It will compute and cache stale data again. This is a race condition.
	- This is solved using cache versioning. Instead of deleting you store a cache with a added keyword of version in the key. How it works is
		- On read
			- Check the current version -> construct the key -> read from cache 
			  -> on miss use the same version to write a new key.
		- On write
			- Start transaction  -> update the db -> increment the version -> add new key with new version
		- What it does is we are avoiding deleting data, now even if race conditions are happening, they would only update the older version and not new ones.
