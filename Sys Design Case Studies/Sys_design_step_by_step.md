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



[Reference](https://www.youtube.com/watch?v=bUHFg8CZFws&t=232s)

