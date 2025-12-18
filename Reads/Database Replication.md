#### Statement-based 

This technique is being used since quite long time. Databases like MySQL uses this.
In a leader-based replication using statement-based technique, two things happen.
- All the writes to the db gets logged as a statement
- The statement gets forwarded to all the followers. 

So all the writes , updates and deletes get forward to all the replicas and gets executed to create an exact copy of the data in leader. There are many advantages to this - 
- Highly efficient from network bandwidth perspective since only SQL statements get send over to replicas.
- Easy to adopt among different versions of the db
- Simpler and easy to use

But there quite a few disadvantages to it. 
- A non-deterministic function being used in the query like `now()`, `rand()` or `uuid()` will not be consistent among all the replicas. 
- For Statements with columns having auto-incrementing all the operations in a transaction needs to be executed in same order to avoid inconsistencies in the database.
- Statements with side effects like triggers and procedures can create unforeseen scenarios in replicas.

#### Shipping the Write-Ahead log (WAL)

The WAL is an append-only sequence of bytes that stores all the info of the writes to the database to ensure durability, performance, and support for transactional integrity of the database. For all the operation the data (such as what data was modified, inserted, or deleted) gets logged into WAL even before executing the changes to database in chronological order(write, delete, update) of operations. 

Append-only here refers to the fact that in the stream of bytes the WAL stores new data always gets appended at the end of the sequence. Its not modified or removed just new bytes gets appended at the end.

Now these WALs can also to transferred to the followers of the leader which then can be used to create an exact copy of the leader into all the replicas

The only disadvantage to this approach is that the data gets stored at a very low level here so the logs can only be made sense if the storage engines are same. So changing the version will make the logs useless. 
So zero downtime upgrade is not possible.

#### Row-based Replication

Row-based replication gets around the storage engine problem by creating a logical log, a sequence of all the writes that happened into the database table row wise. Each record contains the data about the new operation that changed any specific row of the table in db. In case of multiple operations to rows multiple logs gets created. 

- In **case of insert** , it stores all the new values that needs to be added to a row of all columns
- In **case of delete** , it stores the info to uniquely identify the row that gets deleted.
- In **case of update**, it stores all the new values that needs to be updated to a row of all columns and the info to uniquely identify the row that gets updated.

Since this does not depend on storage engine it also supports backward compatibility. 

[Reference](https://newsletter.systemdesigncodex.com/p/database-replication-under-the-hood)

