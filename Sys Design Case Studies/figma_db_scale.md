#### Background

Figma's Postgres database were already vertically partitioned. Groups of related tables like `Figma files` or `Organizations` were further split into their own vertical partitions. This allowed incremental scaling and enough runway for time ahead. 

Vertical scaling couldn't help after a certain point when some of Figma's table started to gain data in terabytes with billions of rows. They tried to quantify the scale by gathering numbers based on historical data and load testing to understand the CPU usage and IO to table and rows written. These numbers were essential to understand when to  prioritize scaling problems before they ballooned into major reliability risks. 

With billions of rows they were at a risk of reliability impact during postgres vacuums, background processing that prevent Postgres from running out of memory and breaking down. With so many writes they were at a very close to running out of IOPS for the largest Amazon RDS. Vertical scaling weren't helping with tables with large data because the smallest unit of partitioning is a table.

#### Scaffolding for Scale

Short term Goals were pinned down to lay a path for long term challenges. Aimed to -
- Databases team wanted to handle all types of complex data models so as to enable minimize application developer involvement.
- Scaling out transparently making sure no changes to the application layer were needed as the product extends with new features after the initial upfront work.
- Skipping expensive backfills considering the shear volume of data in the table would have taken months. 
- Maintaining data consistency and uptime with no choosing to go with complex mechanisms like double writes that would incur overheads and involve downtimes.
- Incremental rollouts to avoid large outages and maintain Figma's reliability.
- Avoid one way migrations which allows rollbacks even after a physical shard completion.
- Leverage strengths by identifying the possible incremental rollout areas and exploring ways we already have expertise in as a team. 

#### Exploring Options

There were options available for open source horizontal sharded enable databases like CockroachDB, TiDB, spanner etc but that would have required migrating figma's huge database which involve a lot of complications and reliability and consistency has to be ensured at two different databases. Also the expertise build maintaining with In House RDS database will also be of no use. So they preferred a low-risk known solution rather than easy uncertain solutions.

NoSQL databases were also a popular choice that offers sharding by default but figma had very complex relation among its datamodels and they did not to indulge application teams to write the entire application layer for this.

So they began to explore building a sharded solution on top of figma's vertically partitioned database. A ground up build of highly generic database wasn't consider but something that was figma requirement specific like they chose not to implement cross-sharded transactions as there were able to handle those failures. A colocation strategy was choose to ensure minimal changes to application layer and which allowed them to support a subset of postgres that was compatible with their application layer. They were also able to support backward compatibility with their unsharded postgres. 

#### Path to Horizontal Sharding 

Splitting a single table or a group of tables into multiple database instances was the key. Once sharding in supported at the application layer , any number of shard splits can be at the physical level. 

![[Screenshot 2024-03-19 at 10.57.44 PM.png]]

Sharding is difficult because as data gets spread across multiple instances, we lose many reliability and consistency features of ACID. There are challenges like - 
- Certain queries being inefficient , complex to implement and something impossible to support.
- Application layer should be updated to support routing of queries to multiple shards as required.
- Database schemas needs to be co-ordinated across the shards to ensure data is in sync. Foreign keys and global indexes are not longer be enforced by postgres. 
- Transactions now became multi shards which causes postgres no longer support transactionality. There could cases to partial update to databases. So the product needs to be logic resilient to such partial commits.

They wanted to lay down the pathway to sharding of multiple tables or group of tables by first sharding their table with most volume which would allow them to extend their runway on their most loaded database. It took the team nine months to shard their first table end to end. 

#### Unique Approach 

**Colos** - Multiple similar tables are sharded together sharing same sharding key and physical sharding layout. The allowed product teams to interact with horizontally sharded tables. 
*Sharding key refers to the column or group of columns which tells which tells which shard a row belongs to. The physical layout includes the decisions of how the shards were created and how they are physically distributed.* 

**Logical sharding** - Figma separated logical sharding with physical sharding which allowed safer and low cost logical sharding rollout with database views and testing before the actual physical failover, which basically refers to the eventual transition from logical sharding to physical sharding.

**DBProxy** -  A dbProxy was built whose job was to intercept the incoming queries from application layer and router them to the specific shards as required. It has the ability to parse and execute 


