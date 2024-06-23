## Chapter 3 - Storage and Retrieval

#### Hash Indexes

Suppose there is a append only file which is used as a database as described in book Page 70. How do we create indexes for those ? 
We can create a in-memory hash-map storing the Byte offset of the key. This way we wont have to look through all the memory to find the key we are looking for. 

![alt text](/resources/Screenshot%202024-04-01%20at%2010.56.34%20PM.png)


Bitcask is one of the storage engines that does similar implementation. Cases where there are a lot of writes and not a lot of unique keys can be useful here.But as we keep appending to a file , it will run out of space. What can be done is breaking a large segment into smaller segment. A certain size can be decided after which a segment will be broken into a separate segment.

Further optimization can be done by compaction. Compaction refers to the fact in which the segment is broken down to only keep the latest updates for each key. Multiple segment compaction can also be done to reduce the segment size further. 

![alt text](/resources/Screenshot%202024-04-01%20at%2011.21.14%20PM.png)


Also each segment now has its own hash-map now with byte offsets and while looking for a key we first look into the most recent segment and if key is not found in that segment we look into the second most recent segment. 

#### SSTables

Suppose we want to sort the segments by key , sorted by the key with the latest update. We can achieve that by forming SSTables or *Sorted String tables*. SSTables have a big advantage in hash-map indexes. 

![alt text](/resources/Screenshot%202024-04-02%20at%2012.21.32%20AM.png)

So from the above we can see from the 3 segments, we are reading them sideways and look at the first key of each segment and take the one with lowest key(as per sorted order of strings) to the output file and then repeating the process by taking the key with latest update in the segments and adding it the final merged segment sorted by the key string. Also if there is duplicates we are taking the key from the latest segment and discarding the rest. 

Now, in order to create the index for this segment we don't need to store value of all the keys and their byte offsets, we can just store the key-offset of some of the keys and see if the required key falls in the range of the 2 keys we know. Then we can scan in between and find the target since now the segment is sorted.

![alt text](/resources/Screenshot%202024-04-02%20at%2012.28.43%20AM.png)

Since now the read request needs to scan a bunch of records in a range anyway, a block can be grouped , compressed and written in the disk which saves disk space and I/O.

##### Constructing and Maintaining SSTables 

To create sorted SSTables we can use a special data structure called Red-black tree or AVL tree. In AVL trees no matter how we insert a value , it can be read in sorted manner. So the storage engine works as follows - 
- When data is inserted into an AVL tree, it gets sorted. This is also called *memtable*.
- When the *memtable* crosses a certain size , say some megabytes , it gets written into the disk. This segment becomes the latest segment and the new entries start forming another AVL tree.
- When some data is read back , its first looked into the in-memory *memtable*, if not found its looked into the latest disk segment then the next latest segment and so on.
- Background processes run to merge and combine multiple segments and to discard overwritten(duplicate) and deleted files.

This has one problem which is if the database crashes the data gets lost so we maintain a log file where data gets immediately appended on insert. Its not sorted though. The log file is deleted when the memtable is written to disk.

##### Making of LSM of SSTables

There are a bunch of databases that use this technique based on Google's bigtable paper. This kind of index structure is actually called log-structured merge tree or LSM.

Lucene , a full text based indexing engine also uses this technique to create an index. A full text engine is much more then an LSM but its similar. *Refer book Page 79.*

##### Performance Optimizations 

A LSM-tree algorithm can be slow if the key is not present in the tree. Since In this case it has to look through the entire tree in memory and all the disk segment. So bloom filters are often used to optimise the search. Bloom filters are memory efficient data structures that approximate the presence of a key in a set.
There are certain compaction strategies are used to optimise the compaction. Some are *size-tiered* and *levelled* compaction. Different databases use different strategies. 
In size-tiered compaction, newer and smaller SSTables are successively merged into older and larger SSTables.
In levelled compaction, the key range is split up into smaller SSTables and older data is moved into separate “levels,” which allows the compaction to proceed more incrementally and use less disk space.
In traditional compaction strategies like "size-tiered compaction," the compaction process involves merging multiple SSTables into larger ones to reduce fragmentation and improve read performance. However, this process can be resource-intensive and lead to temporary spikes in disk usage and performance degradation during compaction. In contrast, levelled compaction breaks down the compaction process into smaller, incremental steps. Each level only contains a certain range of data, so compaction can be applied more selectively and incrementally to smaller subsets of data. This helps to mitigate the impact on disk usage and performance by spreading out the compaction workload over time.

Basically how it works is whenever certain number of level 0 files of size 100MB is there, we merge them as per compaction. Then we wait for the merge file to grow as per level 1 size which is may be 1 GB. So when merged file grows to 1 GB and we have say 10 files of 1 GB we trigger level 1 compaction.

Even though there are many subtleties, the basic idea of LSM-trees—keeping a cascade of SSTables that are merged in the background—is simple and effective. Even when the dataset is much bigger than the available memory it continues to work well. Since data is stored in sorted order, you can efficiently perform range queries.

##### B-Tree

The log-structured indexes has been around but the widely accepted index structure still remains B-Tree. The difference in log structured index and B-Tree is in B-Tree , the database is broken down into fixed-size blocks or pages typically of size 4KB , the structured corresponds to the size of the disk, as disks are also arranged in fixed-size blocks.
The algo of finding a key in the block is below

![alt text](/resources/Screenshot%202024-04-06%20at%207.31.05%20PM.png)

The number of references to child pages in one page of the B-tree is called the ***branching factor***. In this above example its 6.
To update a key in the B-Tree we follow similar algo of finding the key and updating it and writing the page back to disk.

![alt text](/resources/Screenshot%202024-04-06%20at%207.34.11%20PM.png)

To add a new we find the page the key should go to and add it there, if the page doesn't have the required space to accommodate another key ,it is split into two half-full pages, and the parent page is updated to account for the new subdivision of key ranges.
This algorithm ensures that the tree remains balanced: a B-tree with n keys always has a depth of O(log n). Most databases can be accommodated in a 4 level block mostly if the branching factor is set as per requirement. 

[Animation](https://www.youtube.com/watch?v=K1a2Bk8NrYQ&t=22s)

##### Making B-trees reliable

One problems with B-Trees are complicated write and update operations. Suppose while trying to add a new value if a page is split, the parent also needs to be updated with the ref of the children. This is a complicated operation, incase the database breaks it will end up with corrupted index. 
To avoid this, B-Tree uses something called WAL (write ahead log), the WAL is a append only binary stream where every modification needs to be added before committing it to the B-Tree. This way is then used to restore data in case of a database crash. 
One common issue is concurrency. Multiple threads can cause race conditions in the B-Tree causing it to go in an inconsistent state. To avoid this latches (lightweight locks) are used on B-Trees. Its simpler in log-structured case because its append only and overwrites gets removed on compaction.

#### Comparing B-Trees with LSM Trees 

##### Advantages of LSM

One of the issues with B-Tree is that the number writes are higher then LSM which can incur more cost and a probability of space wastage is higher due to unused space is pages. 

##### Downsides of LSM

- Expensive compaction can effect the reads and writes on the LSM. Compaction runs in background but the disk has limited resources.
- Another issue with compaction could be high throughput effecting the compaction which will cause in the increase of segments and eventually increasing the reads times needing to read through a lot of segments.
- Another advantage of B-Tree is unique keys which might not be the case in LSM if compaction is not performed properly. 

#### Storing values within the index

Usually there could be two ways of referencing to the row values from an index. It can either by storing the entire row values within the index or by storing a reference to the place where data is stored. It stores data in no particular order .The data is stored in a heap file. The key advantage of heap file is that it can avoid duplicates since if multiple secondary references are present they will point to the same reference where data is stored.  Any deleted key is tracked and deleted.

While updating without changing the key, the heap approach can be quite efficient since the data can be over-written if the value is same or smaller. In case of larger values there might be a need to copy all to a new heapfile or leave reference in the old file to the new file.

But this approach can be a performance overhead due to the need to jump to a reference to fetch data. This can an overhead as writes might be slower. In SQL , primary indexes store the row values and the secondary indexes refers the primary index. 

A compromise between a clustered index (storing all row data within the index) and a non-clustered index (storing only references to the data within the index) is known as a covering index or index with included columns, which stores some of a table’s columns within the index. This way some queries can just be answered from index itself. 

#### Multi-column indexes

There could cases where multiple indexes needs to be used at the same time. In case of LSM or B-Tree based indexes, only one of them can be accounted for. R-Trees can be a solution to this. Can read more about them out of scope for us here.

![alt text](/resources/Screenshot%202024-04-08%20at%206.22.45%20PM.png)

#### Storing everything in-memory 

One of the major advantages here is the required of encoding to store in disk in not there as we have in disk based storages. It also provides data models that are difficult to implement in disk based storages like priority queues and sets. 

#### Transaction Processing or Analytics?

Databases are expanded into many areas over the areas from earlier being used as a way to track monetary transactions. Databases where the updates are based on user actions like update , delete or read are often referred as *online transaction processing* (OLTP), whereas if they are used for Business analytics which is a very common use case in today's systems they are referred as *online analytics processing*. 

![alt text](/resources/Screenshot%202024-04-13%20at%2010.47.50%20PM.png)


In early days , same database was used for both purposes. SQL databases were a great fit and served the purpose well. But as we moved forward companies stoped using the same database for analytics and started to have a separate database for OLAP-type queries. This database is typically called *data warehouse*. 

#### Data Warehouse

OLTP systems are usually expected to be highly available and with low latency. Running huge analytic queries on such systems can effect the efficiency concurrency reads and writes so OLAP type queries in run on a separate database, a *data-warehouse*, its where the analysts run the queries to draw business insights. Its usually a copy of all the data of all the OLTP systems. 
Data is extracted from OLTP systems , either by periodic data-dump or continuous stream updates, transformed into analytics friendly schemas and loaded into the data-warehouse. This process is called ETL(extract-transform-load). 
One big advantage of warehousing is access patterns can be optimised for analytics.

![alt text](/resources/Screenshot%202024-04-13%20at%2011.09.39%20PM.png)


#### Stars and Snowflakes

OLTP systems can have a wide variety of data models but OLAP data models are usually follow a formulaic style known as star schema. 

![alt text](/resources/Screenshot%202024-04-13%20at%2011.37.32%20PM.png)

The above is a typical example of star schema. In the middle is the *fact_sales* which stores all the events that are happening within the OLTP systems. Extending this are the dimension tables , where each row in the fact table represents an event, the dimensions represent the who, what, where, when, how, and why of the event. The *fact_table* stores the foreign key to the dimension tables.

Another schema is a *snokflake schema* which is a further normalised schema which extends the dimension tables to sub dimension tables. For example, there could be separate tables for brands and product categories, and each row in the dim_product table could reference the brand and category as foreign keys, rather than storing them as strings in the dim_product table. 

Usually star schemas are preferred more as they are simpler to analyze. 

#### Column-oriented database

In analytic systems , column oriented databases are much more efficient then row-oriented databases. The reason being the rows of all the columns are stored together in memory so its much more efficient to load only the values we need without having to load all the row just for one value. 

![alt text](/resources/Screenshot%202024-04-15%20at%2010.43.50%20PM.png)


#### Column Compression

Column-oriented databases can be further optimised by introducing compression using bitmap. Often there are a lot of repetitive values in column oriented databases. 
The distinct values can be taken and bitmap can be created for each distinct value and can be mapped to create bitmaps as below. 

![alt text](/resources/Screenshot%202024-04-15%20at%2010.50.05%20PM.png)

Data compression ensures more caching of data and faster network transmission due to smaller size.

**Dictionary Compression**

In this type of compression what we do is create a dictionary of unique values and store them. Suppose we have a bunch of available school in an area, so in a table to store student details for an area, a lot of repetition of school names can happen, so this can be useful there. 

#### Data Storage Optimizations in Column Oriented Database

In case of column oriented databases, we need to store data in different rows so it needs to be written in a bunch of places(since all the columns are stored together and rows are separate). In order to optimize this, we can implement something like LSM based indexing strategy where we write all the rows to LSM tree and then when it gets too big we bulk write to separate places where the rows are actually stored. 


#### Sort order in Column Storage

Column oriented databases are usually sorted based on the requirement. Suppose we need data of last month sales very frequently , so `date_key` could be a great param to use to sort the database. Secondary sort key could `product_key`.  Also sorting makes it easier for us to compress data. 
There can be different sort keys for different database instances backed in different clusters. They servers the purpose of redundancy and also provides a way to sort them with a different sort key and hence could be used if a different requirement came in.

#### Materialised view & Data cubes 

In relational databases , we have something called views which basically store queries. They are shortcut to writing queries. When the view is queried , the underlying query is used to process. But materialised view is actually a copy of the query results written in disk which gets updated when the underlying data changes. This makes the writes quite expensive which is why not commonly used in OLTP systems

Data cubes are a way to represent data in 2d space in OLAP systems for quick access for reading queries that are frequently used. Its a way to representing precomputed data for performance boost. 

![alt text](/resources/Screenshot%202024-04-18%20at%2011.23.33%20PM.png)



[Mind Map](https://trunin.com/en/2021/12/designing-data-intensive-apps-part03/images/data-intensive-apps-part03-storage-and-retrieval_hu86d7427f9b4c142d70ccb6a3b30f285b_1041367_1815x5119_resize_q90_h2_box_3.webp)








