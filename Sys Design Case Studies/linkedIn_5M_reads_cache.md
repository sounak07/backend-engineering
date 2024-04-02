## How linkedIn servers 5M profile reads a sec

LinkedIn was able to hit a cache rate of 99% which reduced their tail latency and reduced their infra cost by 10%.

##### The History

![alt text](/resources/Screenshot%202024-04-02%20at%209.43.05%20PM.png)

Earlier what linkedIn used to do when a profile is requested , in simple terms the frontend would request the backend for the profile. The backend would make a request to the Espresso, linkedIn's in-house NoSQL db and return.

Espresso also had a OHC(off-heap cache) in the Espresso router. The OHC is quite efficient for hot keys but it is scope limited, meaning it was limited to the router instance. When they tried to scale adding more instances did not really help, the effect on perf was quite diminishing. 

*An off-heap cache is a type of caching mechanism used in computer systems, particularly in Java and other languages where memory management is explicit. In traditional caching systems, data is stored in the heap memory managed by the language's runtime environment. However, in off-heap caching, data is stored directly in the system's physical memory (RAM) but outside of the heap managed by the language runtime.*

##### The big change

![alt text](/resources/Screenshot%202024-04-02%20at%209.56.31%20PM.png)

The architecture shows that the Couchbase sides aside from the Espresso storage node. One of the advantages of this architecture is Espresso handles the internal caching part on its own with any intervention from the application developers.

##### Reads

![alt text](/resources/Screenshot%202024-04-02%20at%2010.07.51%20PM.png)

First the request checks OHC, on cache miss it goes to the couchbase cache , if data found , it returns it else if its a miss it requests the data from the Espresso storage.

##### Writes

![alt text](/resources/Screenshot%202024-04-02%20at%2010.16.08%20PM.png)

Now the cache misses needs to be updated into the couchbase. This is done by Brooklin. Brooklin upserts and streams data to the cache updater to update the cache.
There are two streams in Brooklin. 
- Brooklin Change data capture stream is used to populate the updated row into the cache.
- Brooklin cache bootstrap stream to populate the cache with the frequently created storage snapshot.

Cache bootstrap refers to the process of updating/creating the entire cache at once with the initial data or data snapshots.

##### Design Requirements for Scalability 

**Resilience of Couchbase**

The only resilience for Couchbase was falling back to database. To add a few more solutions linkedIn did a few things.
- Add a health check by the Espresso router on all the Couchbase servers it has access to. The healthiness of the server is decided by comparing the numbers of request exceptions to a threshold. If a server is unhealthy , router would not send request to that.
- In order to implement redundancy , they took 3 replicas of couchbase. 1 leader and 2 followers. If the leader is down , requests are directed to its replicas.
- If the request to the leader failed due to network issues or exceptions , we retry is also implemented.

**High Availability** 

The couchbase needed to be highly available. To ensure that linkedIn cached the profile to all the regions they supported so that in case of data center failure, it can act as a redundant data.
The TTL for that was kept finite time so the used and outdated cache gets deleted.

**Minimizing Data divergence** 

The Couchbase is getting updated by multiple services. We have the cache updated , cache Cache bootstrapper. LinkedIn needed to ensure race conditions does not create data divergence. So they implemented a few workaroungs.

***Ordering of Updates*** 

Each record in cache gets created with a logical timestamp called SCN(System change number). It gets stored in binlog whenever a new row is committed into the database.
Now if there are multiple services trying to update, the one with the latest SCN or largest gets the replace the record in couchbase. 

***Periodic Bootstrapping*** 

This is done to keep the cache updated the database. The update are made in an interval that is less then the TTL so that the data in cache does not get expired before bootstrapping. 

***Handling Concurrent Updates***

In order to handle concurrent updates , couchbase generates something called Compare-And-Swap (CAS). CAS value is typically stored along with cache.
Whenever some data is read from cache , CAS also gets sent with the data. Now if an update is requested CAS needs to be sent to Couchbase , if there is another service that updated the cache before this CAS gets changed and does not match. So its an indicator that the data has been updated and can be handled accordingly. 

![alt text](/resources/Screenshot%202024-04-02%20at%2011.39.57%20PM.png)


[Reference](https://newsletter.systemdesigncodex.com/p/how-linkedin-uses-caching-for-profile-reads)
