## System Design Guide Step by Step


##### Questions to ask/clarify 

![alt text](/resources/Screenshot%202024-06-03%20at%209.04.57%20PM.png)

##### Functional and Non-functional Requirements

*Functional requirements t*ells us what exactly the system will do, specifically APIs. Basically all the functions the system will do to achieve certain goals. 

![alt text](/resources/Screenshot%202024-06-03%20at%2010.52.57%20PM.png)


This shows how we can optimize out APIs to more generic in a step by step improvisations. 

*Non-functional* requirements tells us how the system should be like how fast it should be , its performance, its scale etc. 

![alt text](/resources/Screenshot%202024-06-03%20at%2010.57.18%20PM.png)


Try writing both the requirements at the very start in the board.


![alt text](/resources/Screenshot%202024-06-03%20at%2010.59.10%20PM.png)


##### What do we store ?

![alt text](/resources/Screenshot%202024-06-03%20at%2011.04.05%20PM.png)


This a point where we need to understand the data write and processing intervals. The data processed within few minutes needs to be aggregated on the fly but data that is processed several hours later can be all stored and later processed. 
The former approach is called stream data processing and the later is called batch data processing. 

If we choose to store data in both ways we get best of both worlds. We can choose to store the raw events and calculate real time numbers, we purge the raw data after processing and gathering aggregated data, but doing all this will be more complex and expensive. 

##### Where we store ?

![alt text](/resources/Screenshot%202024-06-03%20at%2011.27.17%20PM.png)


**SQL Solution**

![alt text](/resources/Screenshot%202024-06-03%20at%2011.33.27%20PM.png)


*Cluster proxy* maintains with details of all databases and know to direct traffic to the correct shard. Cluster also needs to know the status of the shards, where a shard died and a new shard took its place. This is done by Zookeeper.

*Zookeeper*, a configuration server monitors and maintains the healthiness of the shards so that the cluster proxy knows which shards are alive and can be used to read/write form.

*Shard Proxy* helps in caching queries, maintain connection pooling, terminate long holding connections etc. 

Data needs to be replicated for availability , this can be either done in sync or async manner.  Here we are following master slave architecture. Writes are on the master shard and reads can be from any. 

To ensure replicated data is available in case of data centre outages, we put some replicas in different data centre to ensure this. 

**NoSQL**

![alt text](/resources/Screenshot%202024-06-03%20at%2011.55.04%20PM.png)


In NoSQL, specifically Cassandra we follow an architecture where each node can talk to each other. We don't need all the shards to talk to each other , each shard can share info with other (not more then 2) every second, this way the info gets propagated to all the shards very quickly. This is called *gossip-protocol*. So now we don't need any cluster proxy since each node knows about each other. 

Whenever processing service calls a node, the co-ordinator node, based on round robin or network distance. The co-ordinator node then decides which node to store the data in based on consistent hashing. 

The co-ordinator node might even choose to replicate the data to all the nodes by calling them parallely but wait only for the success response to come back from 2 nodes to consider it successful. This is called quoram writes. Similarly in quoram reads, the co-ordinator node makes parallel calls to read data from all the nodes. There might be stale data in a node which wasn't updated for some reason. So we need to add handling for that as well. 

Similarly for availability, we need to replicate data to different data centres. 

##### How do we store ?

![[Screenshot 2024-07-29 at 9.46.34 PM.png]]

**Data aggregation Basics**

![[Screenshot 2024-07-29 at 9.53.30 PM.png]]

**Checkpointing and Partitioning** 

![[Screenshot 2024-07-29 at 10.14.12 PM.png]]

Checkpointing refers to the process of saving data at certain points in time to preserve the state to be re-used in case of loss of data. The above example shows how we can use the Checkpointing to restore the data into the cache of processing service if its not saved in db in case of a crash of service

Partitioning is having separate queues to store events which also allows parallel processing of events. A hash can be used to select the query for a particular event. 

**Design Processing Service**

![[Screenshot 2024-07-29 at 10.30.30 PM.png]]

The embedded database stores the meta data around the event that we are trying to store. If its a video event it might have channel name, video title etc. The trick is to keep the database in the same machine to avoid network calls.

The internal queue is to support multi processing and streamline the data storage requests to enhance scalability since processing and storage of data might take some time and adding a queue here ensures streamlines it.

The state store is cache store to store the in-memory cache data and reload it from there.

![[Screenshot 2024-07-29 at 10.37.10 PM.png]]

**More concepts** 

 ![[Screenshot 2024-07-29 at 10.50.27 PM.png]]

To improve the overall performance , we should batch sending data to service. This is to ensure that we are not making too many calls and overloading the service. 

Too many retires can cause the service to overload , to avoid that we use Exponential and jitter algos. Exponential backoff increases the wait time between every retry and jitter introduces randomness into the intervals to spread out the load. 

Circuit breaker pattern basically stops a client from invoking the same request again and again thats bound to fail in certain period of time when the errors cross a certain threshold. After certain amount of time the requests are again allowed and if that request passes without errors, its assumed that the error that was causing the issue has been resolved. But setting the error thresholds are timeouts becomes difficult with circuit breakers. 


**Load Balancers**

Load balancers are usually either hardware based or software based. ELB from AWS is a software LB. These LBs are usually protocol based , it can TCP based or HTTP based.

In TCP LBs, the LBs don't inspect the content of the data. Its like establishing connection between client and server and sending the data packets which allows handling of large scale of data.

In HTTP based LBs, the LBs can inspect the requests are make certain decisions based on the data in the request's headers or cookies. Also these LBs terminate the requests and don't hold them for continuous period of time. 

Health checking is something that LBs use to monitor the nodes and send request accordingly. To ensure high availability ,the concept of primary and secondary nodes are introduced. The primary nodes serves most of the traffic and secondary nodes come into effect if primary ones fail. 

**Partition Service and Partitions**

![[Screenshot 2024-07-29 at 11.18.46 PM.png]]

In order for the partition service to decide which partition to move the message , some strategy needs to be used. This strategy can be of different types one of them could be hashing. But at scale that could lead to hot partitions meaning the video events with very high views could end being pushed into the same queue. To avoid this video time could be added into the partition key. 

Message formats can be either textual or binary formats. 

**Data retrieval Path**

![[Screenshot 2024-07-29 at 11.27.23 PM.png]]

Storing time series data can be complicated. Suppose we are storing events for every minute of the video, thats a lot of data. So with time data aggregation needs to be done and probably move it to a separate type of storage thats rarely accessed as its old. Suppose i would want to show the user only the aggregated data of 1 year old video. 

![[Screenshot 2024-07-29 at 11.33.16 PM.png]]


**Tools**

![[Screenshot 2024-07-29 at 11.36.53 PM.png]]

**Bottlenecks Identification**

- Load testing , soak testing(for memory leaks) can be used. 
- Monitoring - Errors, latency, traffic , saturation. Telemetry is another important one. 
  
Audit systems are very important for visibility of accurate results by system and users. There can be different types of audit systems. 

**Summary**

![[Screenshot 2024-07-29 at 11.48.11 PM.png]]

[Reference](https://www.youtube.com/watch?v=bUHFg8CZFws&t=232s)




