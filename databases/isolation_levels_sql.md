## DB Internals in SQL

#### ACID

[Reference](https://pratikpandey.substack.com/p/database-basics-series-understanding)

SQL databases guarantees ACID based transactions. The ACID stands for -
- **Atomicity** - It guarantees that the transactions are atomic, either its completely done or not. It case of failures , the entire transaction is rolled back.
- **Consistency** - It guarantees that the transactions are allowed to change the state of the database from one to another, leaving it in a state as per certain rules and constraints. 
- **Isolation** - It guarantees that the transactions are isolated from each other to avoid race conditions , dirty reads , bad reads etc. The level of Isolation decides how it maintains data consistency and concurrency. 
- **Durability** - It guarantees the durability of the data once its committed even if the database cluster crashes. This is usually done by logging , redundancy, recovery mechanisms etc.  

Lets talk about the Isolation levels in Details 
#### Isolation levels

There are various levels of Isolation -

**Read Uncommitted** - This type of Isolation level allows you to read uncommitted data by other transactions which might introduce to dirty reads and dirty writes. In this case level of concurrency is the highest but data consistency on reads gets affected. 

Dirty writes refers to writing on uncommitted data. Like for example two people trying to shop something and since writing on uncommitted data is allowed database might end of writing requests from user1 to user2 specific rows.
Prevention can be done by locking of rows. But also need to ensure dead locking is not happening.

Dirty reads refer to reading uncommitted data. Like for example reading change in quantity of items available even before its committed and saying no items available if thats the last one.
Prevention can done by storing the old value unless a commit has happened. 

**Read Committed** - This type of Isolation level allows you to read only committed data by other transactions. This ensure no dirty reads but fails to prevent non-repeatable reads, where reading the same row in the transaction can result in different values being read.

**Write skew**:
*Variant 1* - Lets take an example where we there are a bunch of doctors and at least one doctor needs to action in order for hospital to function. If there is a table with doctor details and there active status. 
To ensure at-least one doctor is active we need to lock on all the active doctors so that we don't end up doing write skew and making all doctors inactive.

*Variant 2 (Phantom write)* - Lets we have flash sale going and we have bunch of items that can be claimed on my one. If two people request at the same time , we might end up allocating the same item to both. 

To avoid this we need to do something called *materialized conflicts*. We basically add rows of all available items to the table and whenever someone requests for the item we put a lock on the row considering its not already taken and then update it to avoid conflicts. 

In both cases they are different from dirty reads as we are not updating un committed data across transactions.

[Reference](https://www.youtube.com/watch?v=eym48yrObhY&list=PLjTveVh7FakLdTmm42TMxbN8PvVn5g4KJ&index=10)
[Reference](https://www.youtube.com/watch?v=oS60pr8H1e0&list=PLjTveVh7FakLdTmm42TMxbN8PvVn5g4KJ&index=8)
[Reference](https://distributed-computing-musings.com/2022/02/transactions-write-skew-why-we-need-serialization/)

**Repeatable Reads** - This type of Isolation level prevents non-repeatable reads, i.e. repeated queries reads would always return the same value. However it fails to prevent phantom reads because of other transactions changing other columns in the database. 

*One example would be user1 added an item to the cart but even before committing the payment, user2 came in and bought it resulting user1 to get an error of item is out of stock.*

***Snapshot isolation*** basically prevents reading wrong data in repeatable reads. Considering a case where a transaction is reading same value again and again we might end up reading different values in different times. The data being read is committed but are different. 
In this isolation, each transaction sees a consistent snapshot which contains all the transactions that were committed before the transaction starts. We are assigning transactions a `transaction_id` while snapshotting and storing them so that we get the old values of rows before this transaction. So when we have a long read we can isolate the transaction based on the snapshot that was created before this the current transaction. 
This is a great technique since there is no locks involved and Snapshot isolation treats read and write operations separately and these two operations don’t block each other at any point.

When there is a deletion of record in any transaction, deleted_by field can be update which basically is populated with `transaction_id` . But the record might not be deleted yet since it might part of some snapshot of previous transaction. So a batch processing needs to be setup and when no transactions is seeing the record it gets deleted. Setting this batch processing is very important otherwise we might end up with lots of deleted records in the memory (also called *bloat*) which might impact perf.

[Reference](https://distributed-computing-musings.com/2022/02/transactions-snapshot-isolation/)

**Lost Updates**

[Reference](https://distributed-computing-musings.com/2022/02/transactions-tackling-lost-updates/)

**Serializable** - This offers the strictest form of Isolation ensuring no dirty reads, non-repeatable reads and phantom reads. This affects the concurrency heavily since it feels like running things sequentially. 

Basically running things in order in a single core instead multi cores. One of the way to fasten things are using stored procedures. Stored procedures are basically present queries or function which only expects params to run them on database. So we are sending a lot less data over the network. But stored procedures are hard to maintain and deploy specially if we have replicas in place.

Some of the issues can be removed by using actual stored procedures to replicate data instead of other ways. But one issue here is the replication needs to be deterministic but created_at col is usually different in this case so this case needs to be handled properly.

**Two Phase locking (2PL)**

It refers to a specific kind of locking on row where reader lock is shared and the write lock is exclusive. 
So multiple transactions can read the row but inorder to update, the transaction needs to wait for other readers to leave the lock in order to attain a write lock and update the db. This resembles to _pessimistic concurrency control_. 

Deadlock on 2PL 
Deadlocks might happen in 2PL in cases where two transactions locking on rows which both of them depend on hence moving to deadlock. [Refer to video](https://www.youtube.com/watch?v=gB7qazeSD3k&list=PLjTveVh7FakLdTmm42TMxbN8PvVn5g4KJ&index=12)

Predicate locks - Instead of locking a single record, lock all records that match the predicate condition. Also no index being present on predicate conditions will slow things further. 
[Refer to video](https://www.youtube.com/watch?v=gB7qazeSD3k&list=PLjTveVh7FakLdTmm42TMxbN8PvVn5g4KJ&index=12)

Index range locking - As with predicate locking we lock based on the predicate condition but in this we use only the indexed rows in the predicate condition to lock rows. This type of locking is faster then predicate because its much faster to find the rows to lock. This comes with the fact that we are locking more rows then necessary , so this should be implemented with caution.

Perf issues in 2PL
Acquiring and releasing locks are expensive so it does introduce latency to systems. Also 2PL does not allow to modify records concurrently so access patterns that require a lot of updates will low things down.
Also long running transactions can get aborted due to deadlocks needs to be restarted with all its resources and context.

[Reference](https://www.youtube.com/watch?v=gB7qazeSD3k&list=PLjTveVh7FakLdTmm42TMxbN8PvVn5g4KJ&index=12)

**Serializable Snapshot Isolation**

This type of isolation tries to evaluate the need for locks if any. If there is going to be isolated transactions where need to locks might not be there. If there is, we might choose to abort and re run those transactions or use different approach in those cases like 2PL.  This can be called a _optimistic concurrency control_.

In a case where concurrent transactions are updating the same values or are conflicting with each using 2PL  is better but if the transactions are isolated which the case most of the time SSI can be used since its much faster then 2PL.
[Refer to video for examples](https://www.youtube.com/watch?v=4TAKYRzm_dA&list=PLjTveVh7FakLdTmm42TMxbN8PvVn5g4KJ&index=14)








