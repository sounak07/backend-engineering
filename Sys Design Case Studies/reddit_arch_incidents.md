## The Evolution of Reddit.com's Architecture


![alt text](/resources/Screenshot%202024-04-28%20at%207.09.17%20PM.png)

#### Listings

Listing are the list of all the posts we see on home page or subReddits etc. The listing are queried from db at first and then the link IDs are cached in the memcache. Then fetch any data on the listing from the db.

When any of the listing were changed it needed to be updated and re-fetched which became slow eventually so they started to update the cache and sort it as per requirement and locks were acquired on these. So read mutate and write operation. The operations are expensive so usually done async using a queue.

![alt text](/resources/Screenshot%202024-04-28%20at%207.18.26%20PM.png)


Doing this makes it something more than cache , its like a denormalised index so they started to store it in Cassandra.

Locking on cached query mutation caused a lot of delay when there were a lot of votes. Using one queue caused the process vying for the lock. So they partitioned the vote queues and used hashing to choose the target queue.

#### Thing

Thing is a data model in Postgres. There is a thing for all components in Reddit like a subReddit thing, a comment thing, a link thing. There is a thing table for all the things.

![alt text](/resources/Screenshot%202024-05-01%20at%204.57.29%20PM.png)


![alt text](/resources/Screenshot%202024-05-01%20at%205.00.24%20PM.png)


So if we see the data table has multiple things. So there is a one-to-many relationship here.

![alt text](/resources/Screenshot%202024-05-01%20at%205.03.38%20PM.png)


**Incident**

![alt text](/resources/Screenshot%202024-05-01%20at%205.11.34%20PM.png)

Reddit started to see inconsistencies in the cache and db after there are incident of replicas crashing. This caused pages to crash a lot. 

![alt text](/resources/Screenshot%202024-05-01%20at%205.13.24%20PM.png)


This is the pseudocode to choose the database. But there's a bug , if the primary is down it would choose the secondary as primary and due to wrong permissions it ended up writing in secondary and write it to the cache listing. So when one of the replicas are taken out to rebuild when crashed , the data is gone, obviously. 

Finally thing was moved out to a separate service. 

#### Comment Trees

Reddit has comment threads where each child can have its own thread, damnnnn. So its quite complicated to store the show these kind of complex comment trees. So some amount of precompute is done. Also comments processing were done via queues. 

![alt text](/resources/Screenshot%202024-05-01%20at%205.22.21%20PM.png)


In order to process comment threads with massive number comments , its marked as Fastlane to get its own processing queue. 

**Incident**
During an event with massive threads, what `Fastlaning` did was it quickly filled up the `Fastlane` queue and kind of filled up the memory of the message broker. So what happened was when thread was switched to `Fastlane` it left out the parent of those comments in the order queue which were not processed so self-healing started kicking in and each page view started to queue itself to get recomputed. 

*Self healing allowed reddit to recompute the comment tree for any missing parent*

![alt text](/resources/Screenshot%202024-05-01%20at%205.31.48%20PM.png)


So Queue Quotas were used to avoid something like. Each queue now has a maximum length on the number of messages it can consume to avoid being overwhelmed. 

#### Autoscaler

Daemons were used to register hosts into Zookeeper clusters. The system is also used to bring up new instances of cache if one died. 

![alt text](/resources/Screenshot%202024-05-01%20at%205.43.14%20PM.png)


Migrating this system from EC2 classic to VPC caused issues. 

![alt text](/resources/Screenshot%202024-05-01%20at%205.44.54%20PM.png)


But the cache servers were also gone and cache servers do not have state since all the older ones were gone. So traffic bombarded the Postgres which its not used it.