Cloudflare handles 20% of total internet traffic. They do it with just 15 postgres clusters. How ?

#### PostgreSQL Scalability

**Resource Usage Optimization**
Cloudflare uses something called Pgbouncer to efficiently manage PG connections.
Pgbouncer is a lightweight connection pooler for PostgresQL. It sits between application and database to efficiently manage pg connections.
It helps prevents Connection starvation and tackles the issues around diverse workloads.

How does it do that though ?
**Connection starvation** refers to the case when multiple clients try to connect with the database and due to the overwhelming requests some client may face delay in connections or connection failures due to resource limitations.
Pgbouncer solves this by maintaining a pool of already established pg connections and by distributing the incoming pg requests.

**Diverse workloads** refers to the cases when multiple tenants tries to connect to a db , some tenants might have a heavy resource requirement of regular writes and some might have a requirement of reads. Pgbouncer makes sure that any single tenant doesn't end of monopolizing the resources by taking up all the available connections in the pool. This can done by adding timeouts, query limits etc to the pgbouncer. So it ensures fair utilisation of resources.

This is how Cloudflare solves the **_Thundering herd Problem_** by throttling the number of pg connections created by a tenant.

**Performance**
Cloudflare runs their postgres on a raw bare metal server without any virtualizations. They use HAProxy as a Load balancer which then directs their request the clusters.

![Screenshot_2024-03-05_at_11.51.42_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2024-03-05_at_11.51.42_PM.png)

**Concurrency**

Too many concurrent requests from tenants could lead to performance degradation.

![Screenshot_2024-03-05_at_11.52.20_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2024-03-05_at_11.52.20_PM.png)

They use _TCP vage Congestion algorithm_ to analyze number of optimal data packets can be sent concurrently.
They do it by analyzing the RTT(round trip time) of transactions from tenants. If the RTT degrades that means there may be some connection issues , so they change the pool size accordingly.

**Ordered queries**
Cloudflare ranks the queries in the Pgbouncer based on their historical resource usage. The ones with high resource consumption are put at the end of the queue.
This is to prevent Connection starvation.
Priority queues are implemented only during peak hours for critical transactions.

**High Availability**

They use a tool called Stolon replicates the primary data to all the postgres instances for high availability. It also elects the leader and does failover in peak traffic

The data replication happens in 2 regions for high availability. Each cluster has 3 databases for each region.
The writes happen in primary region and gets replicated to other regions in async. Reads are directed to those regions.
They use pg_rewind tool to update the missing writes to the primary when it comes back up after failover.

[Reference](https://newsletter.systemdesign.one/p/postgresql-scalability)
