### Scaling Servers

**Vertical scaling vs horizontal scaling**

Vertical scaling, referred to as “scale up”, means the process of adding more power (CPU, RAM, etc.) to your servers. Horizontal scaling, referred to as “scale-out”, allows you to scale by adding more servers into your pool of resources.

When traffic is low, vertical scaling is a great option, and the simplicity of vertical scaling is its main advantage. Unfortunately, it comes with serious limitations.

• Vertical scaling has a hard limit. It is impossible to add unlimited CPU and memory to a single server.

• Vertical scaling does not have failover and redundancy. If one server goes down, the website/app goes down with it completely.

Horizontal scaling is more desirable for large scale applications due to the limitations of vertical scaling.

### Load balancers

Lets suppose there are many servers but all the requests are coming to one server causing high throughput and delay in response.
A load balancer evenly distributes incoming traffic among web servers that are defined in a load-balanced

Users connect to load balancers and don't have a direct access to servers anymore. Load balancers communicate with the servers using private IPs for security. A private IP is an IP address reachable only between servers in the same network. Load balancers uses this to communicate with its connected servers since they are in same private network.

##### Client-Side Load Balancing

With client-side load balancing, the client itself decides which server to talk to. Usually this involves the client making a request to a service registry or directory which contains the list of available servers. Then the client makes a request to one of those servers directly. The client will need to periodically poll or be pushed updates when things change.

Client-side load balancing can be very fast and efficient. Since the client is making the decision, it can choose the fastest server witcohout any additional latency. Instead of using a full network hop to get routed to the right server on every request, we only need to (periodically) sync our list of servers with the server registry.

##### Layer 4 vs Layer 7 Load balancers

![Screenshot_2025-06-04_at_12.50.28_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2025-06-04_at_12.50.28_PM.png)

Layer 4 load balancing makes routing decisions without analysing the data packets, its like randomly picking a server and assuming TCP connections with the server and client. Once established all the subsequent requests would be handled by that server within the TCP connection, this makes this very fast and reliable due to minimal packet inspection and not needing to make a new connection on every request.

This type of load balancer maintains a persistent connection btw the server and client making them useful for cases where maintaining a 2 way connection is important say Web sockets.

![Screenshot_2025-06-04_at_12.52.29_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2025-06-04_at_12.52.29_PM.png)

Layer 7 load balancers are application load balances which has the capability to evaluate the data packets and make routing decisions based on that. This is much more flexible and is much more configurable. Its a bit slow and expensive since it involves CPU computations. It can route based on request content (URL, headers, cookies, etc.).
This type of load balancer doesn't maintain a persistant connection and makes a new connection every time a new request comes in based on data packet evaluation and resource consumption.

This load balancers are best suited for HTTP based connections.

### Cache

#### Cache Tier

![Screenshot_2025-05-16_at_7.10.23_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2025-05-16_at_7.10.23_PM.png)

After receiving a request, a web server first checks if the cache has the available response. If it has, it sends data back to the client. If not, it queries the database, stores the response in cache, and sends it back to the client. This caching strategy is called a read-through cache.

**Considerations for cache** -

- Caching data that is very frequently accessed and is expensive to query. Analyzing the access patterns can be a good way.
- Expiration policy should be implemented to ensure old data is not lurking around my implementing TTL.
- Ensuring consistency about database and cache clusters are crucial.
- Single point of failure is not avoid by having multiple cache servers across regions, say redis can be used as distributed cache server.
- Eviction policy should also be ensured for when cache is full , say LRU(least-recently-used) or LFU(least-frequently-used).

#### Content Delivery Network (CDN)

A CDN is a network servers across regions serving static content to users closet to the server. It usually caches things like HTMLs, PDFs, images videos etc.

Getting from CDN is much faster than getting from the origin as shown below.

![Screenshot_2025-05-16_at_7.30.52_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2025-05-16_at_7.30.52_PM.png)

**Considerations for CDN -**

- CDN can be costly to maintain as its usually provided by third party agencies so analyzing whether product has need for this is crucial.
- Expiration policy implementation is crucial to avoid serving redundant data.
- In case of failures of CDN, a fallback workflow should be in place to ensure availability.

### Data Centres

![Screenshot_2025-05-16_at_7.40.13_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2025-05-16_at_7.40.13_PM.png)

### Messaging Queues

In message queue systems like **RabbitMQ**, concepts like **exchange** and **routing** are central to how messages are delivered from producers to consumers. Here's a clear breakdown:

---

#### 🔁 Exchange and Routing in Message Queues

#### 1. **Producer**

Sends messages to an **exchange** — _not_ directly to a queue.

---

#### 2. **Exchange**

An **exchange** receives messages from producers and is responsible for **routing** those messages to the appropriate **queue(s)** based on certain rules.

There are several **types of exchanges**:

#### a. **Direct Exchange**

- Routes messages to queues based on a **routing key**.
- The message is delivered to the queue(s) whose binding key exactly matches the routing key.

**Example:**

`Routing Key: "error" Queue A is bound with "error" → Message goes to Queue A.`

#### b. **Fanout Exchange**

- Ignores routing keys.
- Broadcasts the message to **all queues** bound to the exchange.

**Example:**

`Queue A, B, and C are bound → All receive the message.`

#### c. **Topic Exchange**

- Routes messages based on **pattern matching** with wildcards (`*` and `#`).
  - `*` matches one word
  - `#` matches zero or more words

**Example:**

`Routing Key: "log.error.db" Queue A is bound with "log.*.db" → Match!`

### Logging, metrics, automation

When working with a small website that runs on a few servers, logging, metrics, and automation support are good practices but not a necessity. However, now that your site has grown to serve a large business, investing in those tools is essential.

Logging: Monitoring error logs is important because it helps to identify errors and problems in the system. You can monitor error logs at per server level or use tools to aggregate them to a centralized service for easy search and viewing.

Metrics: Collecting different types of metrics help us to gain business insights and understand the health status of the system. Some of the following metrics are useful:

• Host level metrics: CPU, Memory, disk I/O, etc.

• Aggregated level metrics: for example, the performance of the entire database tier, cache tier, etc.

• Key business metrics: daily active users, retention, revenue, etc.

### Database scaling

As user base grows scaling the databases out is important to ensure low latency. There can be two ways to scale databases - Horizontal or vertical.

![Screenshot_2025-05-16_at_7.43.25_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2025-05-16_at_7.43.25_PM.png)

#### Vertical scaling

In vertical scaling we increase the resources of the database cluster to keep supporting more and more query requests.

#### Horizontal scaling

In horizontal scaling , an approach of sharding is generally implemented. There can be two ways to do it.

**Horizontal Sharding**

In this database rows are divided into multiple tables with a defined set of rules on how to insert the data on different tables.
Say there are ST1, ST2 , ST3 tables and the rule defines that PK btw 1-10k, goes in ST1, any btw 10k-20k goes in ST2 and so on.

**Resharding data**: Resharding data is needed when

1. a single shard could no longer hold more data due to rapid growth.
2. Certain shards might experience shard exhaustion faster than others due to uneven data distribution.
   consistent hashing can be utilised here.

**Celebrity Problem** - When a single shared in access to many times due to certain access patterns causing the shared to overload.

**Join and de-normalisation** - In case of joining data across tables , sharding could be an issue. It might cause losing the ability to join, de-normalisation of data can help us avoid joins. Its basically adding related data into the shards avoid joins.

**In Sharding Without Denormalization:**

- If `Orders` and `Users` are sharded by `user_id`, some orders and their corresponding users may be on **different shards**.
- Performing a join means **coordinating across shards** – inefficient and hard to scale.

**In Sharding With De-normalization:**

- You **denormalize** the `Users` table into `Orders` like this:

`Orders(order_id, user_id, user_name, user_email, item, price)`

**Vertical Sharding**

Database is usually divided by columns where different columns are stored in different databases.

![Screenshot_2025-05-16_at_7.42.31_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2025-05-16_at_7.42.31_PM.png)
