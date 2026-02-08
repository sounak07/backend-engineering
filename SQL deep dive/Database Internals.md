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
Each row stores meta called xid and ptr, storing the transaction id that modified it and the id pointing to the undo log data for other transactions to refer to. 
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
- Uses predicate locks and lock timeouts
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




#### ACID

**Atomicity**

All the actions in a transaction needs to be treated as an atomic operation.  All these atomic actions should to be completed all at once or nothing at all. The changes done by the queries of a transaction are only visible to other queries/transactions only after they are committed since they are either all(commit) in or nothing at all(rollback even if any of them fail).

![Screenshot_2026-01-30_at_12.33.40_AM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2026-01-30_at_12.33.40_AM.png)


**Consistency**

Every transaction must take the database from one valid state to another adhering the constraints , schemas and invariants. 
Databases enforce this by default, a good error handling from the application side plays an important role.

#### References 
[What are transactions?](https://planetscale.com/blog/database-transactions)
