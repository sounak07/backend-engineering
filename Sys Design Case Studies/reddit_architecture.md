It all started with Lisp but was moved to Python in around 2005. Lisp had a lack of well tested libraries. Starting with web.py and later moving to Pylons. 

#### The Core

![[Screenshot 2024-04-28 at 7.09.17 PM.png]]

**CDN** - The CDN handled a lot of routing logic based on path and domain. 
**Frontend** - Written in Jquery , then moved to Typescript and eventually to node.js based web frameworks.
**The Monolith** - The R2 monolith pretty much supported all the services like Search , listing , Thing etc. 

Reddit moved to AWS from physical servers in 2009 moving their batch processing to EC2.

#### The R2

![[Screenshot 2024-04-28 at 7.18.26 PM.png]]

Same code was copied and deployed to multiple servers to enhance scalability. The load balancer did the job to route the request to appropriate server. Reddit uses Postgres for its core data with memcache servers placed before the database. Expensive operations are usually handled asynchronously using Rabbitmq. Reddit started to Cassandra a lot for its new features. 

#### The Expansion 

In 2017 Reddit started to adopt GraphQL and in 4 years the monolith was completely adopted it. GraphQL is a API specification which allows the client to specify what data do they need allowing clients the flexibility. 

Later they moved to GraphQL federation with a certain number of Goals - 

- Retiring the Monolith 
- Encouraging separation of Components 
- Improving Concurrency

GraphQL federation refers to a system where multiple small GraphQL APIs(called subgraphs) are combined together to create a bigger GraphQL API (called supergraph) which acts as a central point to handle all the requests. 

The Supergraph has the ability to route to whichever subgraphs have the data , send the request to gather it and eventually combining the data from all the subgraphs and send it to the client. 
In 2021 reddit started to add Go subgraphs for components like subreddit , comments etc to eventually retire the monolith. 

![[Screenshot 2024-04-28 at 7.48.03 PM.png]]

One the major requirements for this was migration of data from monolith to Go subgraphs. Reddit wanted to do this incrementally to Go subgraphs. 
They want to ramp up traffic gradually to evaluate error rates and latencies while having the ability to switch back to the monolith in case of any issues
But GraphQL federation did not have a way to accommodate this so they went ahead with Blue/Green subgraph. 

![[Screenshot 2024-04-28 at 7.55.45 PM.png]]

In this way the Python monolith and the Go subgraphs shared the schema ownership. The load balancer in between controlled the percentage of traffic handled by the monolith and subgraphs. 

#### Data replication with CDC and Debezium 

Reddit earlier used WAL to replicate data in the replica. They used a special tool to archive and upload the WAL to S3 for the replica to read. This method a bunch of issues like replication lag due to snapshot timings, fragile replication due EC2 handling backups to S3, Frequent schema changes caused snapshotting issues.

They moved to CDC data streaming with Debezium and Kafka connect. Any updates to the tables will be captured by Debezium which will be uploaded to Kafka connect and a downstream connector reads from kafka topic and updates to target tables. This allowed real-time data replication for reddit. 

*Note : A downstream connector in the context of Kafka refers to a component or application that consumes data from a Kafka topic and processes it further downstream in the data processing pipeline.*

![[Screenshot 2024-04-28 at 8.29.48 PM.png]]

#### Media metadata at Scale

Reddit has a huge dataset of content which includes images, videos, gifs etc. The entire content management was very scattered and unmanageable. There were several problems to it like -
- Content scattered and distributed across multiple systems. 
- No proper format of storage causing varying query patterns even querying to S3 to fetch certain meta data. 
- No proper auditing for content , no way to analyse or update the existing content.

Reddit started to built new system with following abilities - 
- Bringing all data under one roof. 
- Support low latency meta data reads
- Support analyse , data creation and updates. 

![[Screenshot 2024-04-28 at 8.49.58 PM.png]]

The major challenge was to migrate the existing data to new systems ensuring all systems are running. To enable this 

- Dual reads , writes and monitoring was enabled
- Backfill process was enabled. 
- Ramping of traffic to new systems with the ability to fall back to older system was ensured. 
 ![[Screenshot 2024-04-28 at 8.52.45 PM.png]]
