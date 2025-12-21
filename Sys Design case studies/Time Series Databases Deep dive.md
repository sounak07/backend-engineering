[My System Designs](./My_System_Designs.md)

![Screenshot_2025-12-21_at_8.31.18_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2025-12-21_at_8.31.18_PM.png)

How do we store data similar to above, basically CPU/memory metrics considering there would be huge number of writes? 
SQL cannot store these many events, if we do it would be super expensive, even with sharding, costs won't come down; and a basic the data query will put a huge load on the server. So SQL isn't really the right choice to solve this problem. 

##### Append-Only Storage

![Screenshot_2025-12-21_at_10.33.05_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2025-12-21_at_10.33.05_PM.png)

Random access be it to memory or disks are slow, but if we manage to store them in sequential manner, say an append-only storage, fetching would be much faster. 
But how do we organise the append-only storage so the search is quick and efficient. 
We use LLM trees. 

##### LSM and SSTables

![Screenshot_2025-12-21_at_10.56.16_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2025-12-21_at_10.56.16_PM.png)

When the data comes in put that in WAL to avoid the data being lost, once thats done the next step is to put the data into a memtable to organise them. We can choose to create some indexes, reorganise the memtable as per the incoming data or even delete from it. Once they become big enough we flush them into the disk in the form of SSTables. 

An LSM(Log-Structured Merge Tree) uses **SSTables** (Sorted String Tables) as its core on-disk storage, where SSTables are immutable files holding sorted key-value pairs, enabling fast sequential writes and efficient data merging through compaction, while reads involve searching multiple SSTables and an in-memory memtable for the latest data.  How it Works Together:
1. **Writes (Fast):** New data first goes to an in-memory memtable. When full, it's flushed to disk as a new, sorted SSTable.
2. **SSTables (Immutable):** These disk files store data sorted by key, simplifying lookups and merging. Once written, they don't change.
3. **Reads (Multi-Level):** A read checks the Memtable first, then sequentially checks SSTables (newest to oldest), using indexes (like Bloom filters) to quickly skip files that don't contain the key.
4. **Compaction (Merge):** Background processes merge smaller SSTables into larger, more organized ones, removing old data and "tombstones" (markers for deleted data) to keep data fresh and efficient.

##### Delta encoding

![Screenshot_2025-12-22_at_12.20.51_AM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2025-12-22_at_12.20.51_AM.png)

One of the tricks we can use to store data in database is to store the delta instead , say in the example of temperature or timestamps, leading us to store much smaller values taking up less space and involving better compression. 
If we store delta of deltas that even more uniform and easy to compress considering the recorded timestamps are at regular intervals.

##### Time-Based Partitioning


