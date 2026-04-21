#### Transactions in databases

A transaction is a sequence of actions performed on a single database on an atomic operation. An individual transaction can include one or more queries executing is sequence. 
A transaction is SQL starts with `BEGIN` and ends with a `COMMIT`. 

We know that each transaction needs to follow the ACID properties, meaning its should be ***atomic***, either all queries execute with success or none is executed or rolled back. 
It should take the database from one ***consistent*** state to another, the transactions should in **isolation** and the data updated/added by them should be **durable**, should persist even after server crash. 

When multiple transactions are running together, databases need to ensure that other transactions are not reading a stale/outdated data, while other transactions update them before committing. Different database adopt different approaches. 

**Postgres** - ***Multi-row versioning***

Postgres uses something called ***Multi-row versioning***. Each row maintains something called xmin and xmax for each row. When transaction A updates the data in any of the row, a new version of the row with xmin > 0 is created. 
Transaction B continue to read the older version since xmax for that version is 0. 
Now the when transaction A commits, the xmax for the older version to updated with the xmin of new version, now when any transaction tries to read the updated row, its finds xmax > 0 and looks for the updated row which is the xmin of the newly updated xmax value. 
This way Transaction B never reads the updated data until committed during `REPEATABLE READ` situations. 

With time as these outdated rows keep increasing, a command vaccumm is not run compaction to remove those rows and reclaim the space back.

![Screenshot_2026-02-07_at_5.40.38_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2026-02-07_at_5.40.38_PM.png)

**MySQL** - ***Undo log***

MySQL doesn't have the concept of updated and outdated rows, MySQL updates the rows instantly but maintains something called undo log storing the previous values for the other transactions to check. 
Each row stores meta data called xid and ptr, storing the transaction id that modified it and the id pointing to the undo log data for other transactions to refer to. 
This approach removes the extra layer of maintenance of compaction. 

![Screenshot_2026-02-07_at_6.36.19_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2026-02-07_at_6.36.19_PM.png)
##### Killing Transactions in databases

**Deadlock**

![Screenshot_2026-01-30_at_12.05.43_AM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2026-01-30_at_12.05.43_AM.png)

##### 🛠️ How databases deal with this

**MySQL**

- Actively detects cycles(the circular dependency basically) in lock dependencies
- Automatically **kills one transaction**
- Releases its locks so the other can continue

**PostgreSQL**

- Uses a more **optimistic approach**
- Uses predicate locks and lock timeouts. These locks are not used to block access to rows but rather to check what rows are being modified by which transaction.
- Allows transactions to proceed
- At commit time, if a conflict is detected:
    - One transaction commits
    - The other is rolled back

Different strategies, same goal: **ensure the system keeps moving**.

**Dining Philosophers — the timeless analogy**

![Screenshot_2026-01-30_at_12.22.47_AM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2026-01-30_at_12.22.47_AM.png)


##### Isolation levels 

**Serializable** - This type isolation level is the strictest, it acts as if transactions are run sequentially, in real though the transactions are ran sequentially with the help of strong locking and waiting. 

**Phantom reads** - 

When a select query in a transaction running multiple times reads different values due the values being modified by a different transaction. 


![Screenshot_2026-03-05_at_12.28.06_AM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2026-03-05_at_12.28.06_AM.png)

[More details](obsidian://open?vault=reactivist's%20vault&file=engineering_brain_fork%2FEngineering%20Notes%2FSQL%20deep%20dive%2FIsolation%20Levels%20in%20SQL)
#### ACID

**Atomicity**

All the actions in a transaction needs to be treated as an atomic operation.  All these atomic actions should to be completed all at once or nothing at all. The changes done by the queries of a transaction are only visible to other queries/transactions only after they are committed since they are either all(commit) in or nothing at all(rollback even if any of them fail).

![Screenshot_2026-01-30_at_12.33.40_AM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2026-01-30_at_12.33.40_AM.png)


**Consistency**

Every transaction must take the database from one valid state to another adhering the constraints , schemas and invariants. 
Databases enforce this by default, a good error handling from the application side plays an important role.


#### Sharding in databases

Sharding is basically breaking the database down into multiple databases and splitting the data among them to handle the load on too much of data. 

![Screenshot_2026-04-21_at_10.29.00_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2026-04-21_at_10.29.00_PM.png)

Shared key and distribution strategy plays an important role in creating an efficient sharded ecosystem to avoid hot shards.

![Screenshot_2026-04-21_at_10.40.24_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2026-04-21_at_10.40.24_PM.png)

user_id as key in social media makes more sense, while its order_id for ecom. 
Keys like created_at and is_premium does not make sense as they would create too much pressure on a specific shard. 

**Hash based sharding**

![Screenshot_2026-04-21_at_10.43.59_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2026-04-21_at_10.43.59_PM.png)

**Directory Based sharding**

![Screenshot_2026-04-21_at_11.08.32_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2026-04-21_at_11.08.32_PM.png)

##### Challenges in shard

**Hot shards**

Shards which gets a lot of traffic due to may a lot of keys ending up there could lead to hot shards. We can randomise the hash keys by adding a fixed string before hash key.
Celebrity shards can also be used where we create a completely separate shard key for use-cases with huge traffic. 

![Screenshot_2026-04-21_at_11.15.16_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2026-04-21_at_11.15.16_PM.png)


**Cross shard queries**

Queries that require data from multiple shards might lead to slow queries trying to fetch data. 

Caching is one way to eliminate that. Tradeoff here is users might get outdated data if they query is being done within the ttl time.

![Screenshot_2026-04-21_at_11.18.05_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2026-04-21_at_11.18.05_PM.png)

Denormalisation is another way. In case we need to visit the same shards again and again, we can try to club the data from 2nd shard and put it in 1st. This way we avoid doing cross shard queries but we need to write in both shards so the writes become a bit more complex, a trade off we need to consider. 

![Screenshot_2026-04-21_at_11.22.52_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2026-04-21_at_11.22.52_PM.png)

**Maintaining Consistency**

![Screenshot_2026-04-21_at_11.27.27_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2026-04-21_at_11.27.27_PM.png)

Maintaining consistency in data across multiple shards which are part of a single transaction is a huge pain. The textbook way handle is 2 phase commit but that needs a co-ordinator and production systems try to avoid them. Aim to may be avoid cross shard transaction at together.

**Sage Pattern**
It states that each action has a opposite compensating action in case the action fails. In our example, in case the transaction post money deduction fails, we don't rollback we identify the compensating action and run it. 

##### When to use shards ?

- Storage - Very high storage
- Write throughput - Very high write rate 50k writes/sec.
- Read throughput - Read replicas fail to handle the requests.

You dont always need to shard. If you do, propose the following - 

- Propose a shard key - wrong key could lead to bad outcomes
- Choose a distribution strategy - usually its consistent hashing
- Discuss the trade-offs - caching, celebrity shards, cross shard queries
- Discuss how to handle the growth - Add X shards, add more later , redistribute using consistent hashing. 
#### References 
[What are transactions?](https://planetscale.com/blog/database-transactions)
[Sharding by Hello Interview](https://www.youtube.com/watch?v=L521gizea4s)
