##### User data

When a user creates a profile , the data gets added to a key value store database like Dynamo db. Dynamo streams are used to send  changes to a table to other places. 
The data also gets queued to be added to location index which is used to find the nearby people. 

##### Nearby People 

Its hard to find near people just by using longitude and latitude of a person. Grids can be used here but equally spaced grids can create a **hot-shard** situation since some grids might be empty and some have a lot of users.
We use S2, which a hierarchical geospatial indexing. Its helps find the nearby people and also shard the database.
S2 divides the earth into hierarchical grids in which each grid having a unique number. The grids are hierarchical ranging from square-centimetres to square-kilometers. 
Users in nearby location are stored together in a shard to avoid querying multiple shards to get nearby users. It supports grid find by long and lat and also has the facility to return all the nearby grids. 
All the relevant shards are queried in parallel to find the nearby users. On average they query 3 database shards to find people in 160 km radius around them. Finally hits are filtered based on user preference. 

##### Passport in Tinder

Passport lets users change their location to their preference. When user changes their location they again go through the process of adding data to location index. The old location also gets removed from the location partition , which means the user gets sent to a different shard as per the location and grid.

There could be cases where user immediately moves back to their original location after selecting new location , since these events aren't atomic there could a possibility of data inconsistency as the operations are not executed in correct order so the user remains pointed to the new location instead of original after abrupt change. 

This problem is solved by Kafka. Kafka allows data to be processed in order. These change events for same user are sent to same partition in Kafka. Partitions allow Kafka to parallelize data storage and processing, distribute load across multiple servers (brokers), and scale horizontally. Now the Kafka consumers acquire a lock on the partition, this means that while one consumer is processing updates from a partition, other consumers cannot access the same partition simultaneously. This ensures that updates are processed by consumers in an orderly manner, without conflicts giving a FIFO which allows data to be processed in order with very high throughput. 

##### Swipes and Match

When the user keeps swiping the data gets sent to data stream services like Amazon kenesis. Then match workers are user to check from the likes cache to see if their is a match. If there is websockets are use to update the user giving a peer to peer live communication. 
The dislikes from user are put in S3 to analyse and provide better profile recommendations.

##### Problems

Tinder uses unique numbers of users to count the load in a shard. But the users from a shard usually belong to same locations. So there could be traffic parity in a different shards across different time zones. This can cause the hot shard problem. So a single shard to a single physical server could overload the server, so multiple similar shards are randomly assigned to physical servers to mitigate this issue. 
Tinder uses redis to cache users and use set-aside caching strategy which means if there is a cache miss its gets read from db and gets updated in cache.

![alt text](/resources/Screenshot%202024-03-30%20at%2012.14.41%20PM.png)

Writes in a shard are rate limited and Exponential Backoffs are also used.

[Reference](https://newsletter.systemdesign.one/p/tinder-architecture)