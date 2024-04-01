 
#### Thinking Data systems
- Databases, queues and caches are usually referred as data systems even though they have different purposes and access points since they can used to serve each other's purpose since with modern requirements they no longer neatly fit into traditional categories. 
- All the tools above can be stitched together with application code to bring out certain outcome.

![[Screenshot 2024-01-21 at 1.30.53 PM.png]]

*The above example shows how a bunch of tools a message queue , a caching service and a full text search (Elastic) can used together to get a desired outcome.*
*All of which is hidden behind the API.*

#### Reliability

A system can called reliable if -
- It can perform the desired task.
- Its fault tolerant , meaning even if the user makes any mistakes it should be able to handle that. 
- It should be able to perform its desired output even at high load and data volumes. 
- It should be able to protect itself from hackers and un authorised access. 

*How much fault tolerant a system can be ?*

- Failures and faults are not exactly same. Failures prevent the system to produce its desired output or give service to the user, which should not happen.
- Its impossible to design a system to  have fault tolerant for every case out there. The goal here should be to have the fault tolerance for failures so it continues  to provide service without going down. 
- Counterintuitively, in such fault-tolerant systems we actually increase faults in-order to ensure that the fault-tolerance machinery is continually exercised and tested, which can increase out confidence that faults will be handled correctly when they occur naturally.

#### Scalability 
##### Describing Load

Certain parameters called *load parameters* are required in order to describe load. It could depend on the architecture of the system. Parameters could - 
- Requests/sec into the web server 
- Read/write ratio to databases
- Rate of cache hits
- No of concurrent active users in the chat room.
- No of parallel requests a server can serve at a time.  
  
  As per twitter case study mentioned in the book, the second approach which was to maintain a cache of user's timeline and whenever a new tweet is added by someone they follow , that tweet is inserted into the timeline cache of all of the tweet sender followers.
  
  The issue in this is that with high number of followers , the writes to cache timelines increases multiple times. So here the *load parameter* is the distribution of followers. 

##### Describing Performance 

Performance can be investigated in two ways - 
- When you increase the load without increasing the resources , how is the performance changing ? 
- How much resources needs to be added in order to keep up with the performance?
  
  In batch processing systems throughput is a major parameter, ***which refers to the number of records processed per second.*** But in case of systems like online learning response time is a major parameter, which refers ***to the time between a client sending a request and receiving a response.***

*Latency and response time are often used synonymously, but they are not the same. The response time is what the client sees: besides the actual time to process the request (the service time), it includes network delays and queueing delays. Latency is the duration that a request is waiting to be handled—during which it is latent, await‐ ing service*

Random addition of latency could increase the response time causing delays even if all the parameters are same in a different request where it took less time. 

Response times are usually measured based on the median of the requests in a certain time period. 

- p50 says that 50% of the requests Xms , and rest took for then that. 
- p99 says that 99% of the requests Xms , and rest took for then that. 
  
Optimising to improve the rest 1% might be worth it or might not be depending on the business requirements. e.g. amazon case study can be found in book. 

Queuing can introduce a lot of delays in the requests since the CPU threads can only process a certain number of requests. Even delay in a small number of requests could increase the overall response time since it will hold up the processing of subsequent requests—an effect sometimes known as *head-of-line blocking*.

In order to measure the response times the client needs to continuously send requests to the server without waiting for the response so as to take in account the above scenario and hence real world. 
In order to correctly monitor response times a rolling window of say 10 mins can be used and p95, p99 for that can be looked in.

##### Approches to handle load 

Server scaling is usually done in two ways :
- Vertically - Increasing the resources of the machine with load
- Horizontally - Increasing the number of virtual machines with load.
  
A mixture of two should be preferred as going with anyone of them could be expensive.

Architecture design for a system is very specific and usually not generic. A design can't be universally applied to multiple systems since the design depends on lots of factors like data volume , data complexity, response times, logic computations , access patterns etc..

#### Maintainability

##### Operability: Make Life Easier for Operations.

Certain steps can be taken to ensure smooth operations that include - 
- Keep software up to date
- Keeping up with the security patches of the service 
- Setting up monitoring systems for the services
- Writing proper documentation of services
- Setting up tools to anticipate major crashes 
- Establishing good tools and practices for deployment. 
  
##### Simplicity: Managing Complexity 

As the system grows it starts to become more complex. Its important to manage the complexity so that its easier to understand and work with for other devs.
Complexing is introduced by various factors like bad code quality , hacks for performance, forcing services to do things its not intended to etc.

Reducing complexing does not mean removing features , its more about making the overall architecture simpler and easier to extend and maintain.

One of the best ways to solve complexity is abstraction. Abstracting out components can be very useful while trying to work on the high level stuff that service involves in without actually diving deep into individual components. 
This makes components easier to maintain and reuse , reducing the complexity.

##### Evolvability : Making Change easy 

Its extremely important to build systems that can extend very easily without introducing tones of complexity. *Agile* is a way to go to ensure workflow to do that, the community has also developed certain tools and techniques to help teams achieve this.
Abstraction and simplicity are some of the ways which allows easy extensions to systems. 


***END*** 


[Mind Map](https://trunin.com/en/2021/12/designing-data-intensive-apps-part01/images/_hud894c3e2c597300ecc51f8db9caf3c36_547547_0033f68c5cde84a1c81ce95c209e44a5.webp)






