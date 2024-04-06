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
There are certain compaction strategies are used to optimise the compaction. Some are *size-tiered* and *leveled* compaction. Different databases use different strategies. 
In size-tiered compaction, newer and smaller SSTables are successively merged into older and larger SSTables.
In leveled compaction, the key range is split up into smaller SSTables and older data is moved into separate “levels,” which allows the compaction to proceed more incrementally and use less disk space.
In traditional compaction strategies like "size-tiered compaction," the compaction process involves merging multiple SSTables into larger ones to reduce fragmentation and improve read performance. However, this process can be resource-intensive and lead to temporary spikes in disk usage and performance degradation during compaction. In contrast, leveled compaction breaks down the compaction process into smaller, incremental steps. Each level only contains a certain range of data, so compaction can be applied more selectively and incrementally to smaller subsets of data. This helps to mitigate the impact on disk usage and performance by spreading out the compaction workload over time.

Even though there are many subtleties, the basic idea of LSM-trees—keeping a cas‐ cade of SSTables that are merged in the background—is simple and effective. Even when the dataset is much bigger than the available memory it continues to work well.

##### B-Tree

The log-structured indexes has been around but the widely accepted index structure still remains B-Tree. The difference in log structured index and B-Tree is in B-Tree , the database is broken down into fixed-size blocks or pages typically of size 4KB , the structured corresponds to the size of the disk, as disks are also arranged in fixed-size blocks.
The algo of finding a key in the block is below

![alt text](/resources/Screenshot%202024-04-06%20at%207.31.05%20PM.png)

The number of references to child pages in one page of the B-tree is called the ***branching factor***. In this above example its 6.
To update a key in the B-Tree we follow similar algo of finding the key and updating it and writing the page back to disk.

![alt text](/resources/Screenshot%202024-04-06%20at%207.34.11%20PM.png)

To add a new we find the page the key should go to and add it there, if the page doesn't have the required space to accommodate another key ,it is split into two half-full pages, and the parent page is updated to account for the new subdivision of key ranges.
This algorithm ensures that the tree remains balanced: a B-tree with n keys always has a depth of O(log n). Most databases can be accommodated in a 4 level block mostly if the branching factor is set as per requirement. 

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







