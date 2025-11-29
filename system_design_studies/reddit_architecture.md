## Reddit's Architecture

It all started with Lisp but was moved to Python in around 2005. Lisp had a lack of well tested libraries. Starting with web.py and later moving to Pylons. 

#### The Core

![alt text](/resources/Screenshot%202024-04-28%20at%207.09.17%20PM.png)


**CDN** - The CDN handled a lot of routing logic based on path and domain. 
**Frontend** - Written in Jquery , then moved to Typescript and eventually to node.js based web frameworks.
**The Monolith** - The R2 monolith pretty much supported all the services like Search , listing , Thing etc. 

Reddit moved to AWS from physical servers in 2009 moving their batch processing to EC2.

#### The R2

![alt text](/resources/Screenshot%202024-04-28%20at%207.18.26%20PM.png)


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

![alt text](/resources/Screenshot%202024-04-28%20at%207.48.03%20PM.png)


One the major requirements for this was migration of data from monolith to Go subgraphs. Reddit wanted to do this incrementally to Go subgraphs. 
They want to ramp up traffic gradually to evaluate error rates and latencies while having the ability to switch back to the monolith in case of any issues
But GraphQL federation did not have a way to accommodate this so they went ahead with Blue/Green subgraph. 

![alt text](/resources/Screenshot%202024-04-28%20at%207.55.45%20PM.png)


In this way the Python monolith and the Go subgraphs shared the schema ownership. The load balancer in between controlled the percentage of traffic handled by the monolith and subgraphs. 

#### Data replication with CDC and Debezium 

Reddit earlier used WAL to replicate data in the replica. They used a special tool to archive and upload the WAL to S3 for the replica to read. This method a bunch of issues like replication lag due to snapshot timings, fragile replication due EC2 handling backups to S3, Frequent schema changes caused snapshotting issues.

They moved to CDC data streaming with Debezium and Kafka connect. Any updates to the tables will be captured by Debezium which will be uploaded to Kafka connect and a downstream connector reads from kafka topic and updates to target tables. This allowed real-time data replication for reddit. 

*Note : A downstream connector in the context of Kafka refers to a component or application that consumes data from a Kafka topic and processes it further downstream in the data processing pipeline.*

![alt text](/resources/Screenshot%202024-04-28%20at%208.29.48%20PM.png)

#### Media metadata at Scale

Reddit has a huge dataset of content which includes images, videos, gifs etc. The entire content management was very scattered and unmanageable. There were several problems to it like -
- Content scattered and distributed across multiple systems. 
- No proper format of storage causing varying query patterns even querying to S3 to fetch certain meta data. 
- No proper auditing for content , no way to analyse or update the existing content.

Reddit started to built new system with following abilities - 
- Bringing all data under one roof. 
- Support low latency meta data reads
- Support analyse , data creation and updates. 

![alt text](/resources/Screenshot%202024-04-28%20at%208.49.58%20PM.png)

The major challenge was to migrate the existing data to new systems ensuring all systems are running. To enable this 

- Dual reads , writes and monitoring was enabled
- Backfill process was enabled. 
- Ramping of traffic to new systems with the ability to fall back to older system was ensured. 

![alt text](/resources/Screenshot%202024-04-28%20at%208.52.45%20PM.png)

#### Image Optimisations 

![alt text](/resources/Screenshot%202024-04-28%20at%209.08.47%20PM.png)


Reddit needed to serve users across different types of format like mobile, web etc.
Reddit moved from third party Just-in-image optimisations to in-house. They were mainly two services. One to convert GIF to MP4 since GIF aren't optimize friendly due to larger size and higher computation resource. 

#### Real-time Protection for Users at Scale

One of crucial features of reddit was content moderation. Reddit built a system called Rule-executor-v1 (REV-1) to enforce certain rules dictated by the content moderation team. The rules could be a Lua script like below 

![alt text](/resources/Screenshot%202024-04-28%20at%209.30.21%20PM.png)


However this system had some issues to it. This includes - 
- REV-1 spawned a new process for all the new rules that was enforced which needed to be scaled vertically. 
- Lack of staging env for sandbox testing
- Rules are version controlled so no way to track the changes.

A new system was built to address the following issues. In 2021, a new streaming service called snooron was built.

![alt text](/resources/Screenshot%202024-04-28%20at%209.34.38%20PM.png)

Keys differences in REV-1 and REV-2
- In REV-1 all the rule addition were web based but for REV-2 it was done at code level with a UI to make the process simpler.  
-  In REV-1 , Rules are stored in Zookeeper but in REV-2 a github repo was used which enabled the version control for auditing. 
- In REV-1 each rule enforcing spawned a new process caused scaling issues. But in REV-2 it uses Flink stateful functions for handling the stream of events (rules that were enforces) and a separate Baseplate application that executes the Lua code.
- In REV-1 actions triggered by rules are handled by r2 but in case of REV-2 , it sends out structured protobuf actions to action topics to carry out these actions using a new service built using Flink Statefun called Safety actioning worker. 

#### Reddit's Feed

Reddit's feed was a crucial part. Also it needed to be - 
- The dev needed to be faster and should scale well since a lot of teams engage with feeds to support their services.
- Time to interact needed to be faster to enhance user experience. 
- Feeds should be consistent.

Earlier all the posts were a huge Posts object storing everything which wasn't very performant. Later Reddit moved to Server Driver UI which where only the title and description was sent on load.
#### From Thrift to GRPC

Reddit used thrift to communicate between its services. Thrift provides an Interface(or API) to communicate with other services. With growing number of services Thrift became expensive to use. So Reddit's move to grpc was made. Grpc was certain advantages like its native support in HTTP2 , its native support for service mesh tools like istio etc

![alt text](/resources/Screenshot%202024-04-28%20at%2010.24.13%20PM.png)


Reddit used an architecture to mock the Thrift workflow is order to reuse its existing implementation.  

[Reference](https://blog.bytebytego.com/p/reddits-architecture-the-evolutionary)

