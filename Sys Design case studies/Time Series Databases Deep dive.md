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

A concept in Time series databases where data is partitioned based on the time of insertion. The partition can be per day or per week. The partitions can either live in the same machine or in different machines as per the scale. This is very powerful because 
- Writes to partitions become very simple as there is no need to figure out the partition the write should go to.
- Reads are easier and simple since lookup needs to be run on a particular set of partitions based on the range data we are looking for. 
- Retention becomes trivial. Say discarding last 7 days of data becomes very easy

```
┌─────────────────────────────────────────────────────────┐
│  Query: "Last 2 hours of CPU data for host-42"          │
└─────────────────────────────────────────────────────────┘
                         │                                 
                         ▼                                 
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ Nov 22  │ │ Nov 23  │ │ Nov 24  │ │ Nov 25  │ │ Nov 26  │
│  skip   │ │  skip   │ │  skip   │ │  skip   │ │ ← SCAN  │
└─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
```

This is a universal strategy for all Time series databases. 

##### Bloom filters for read optimizations 

A bloom filter is a probabilistic data structure which is capable off telling if a key is there in a probabilistic manner, it can either tell that with "definitely there" or "may be there". If its a may be we can search for it and try to find out if they key is there, otherwise proceed accordingly.
Each SSTable maintains a bloom filter of all the keys to handle the reads, the database always checks the bloom filter first to make a decision, when we query for a series. 
One of the major advantages of bloom filter is how less disk space it requires to store a key, only 10 bits. This is a game changer for millions of series of SSTables. 

```
Query: "Get data for host=server-42"

SSTable-1 Bloom filter: "not here"     → skip (no disk read)
SSTable-2 Bloom filter: "not here"     → skip (no disk read)
SSTable-3 Bloom filter: "maybe here"   → check (disk read)
SSTable-4 Bloom filter: "not here"     → skip (no disk read)
```

##### Downsampling and Rollups

Downsampling basically refers to reducing the number of data points are averaging them out as the data becomes older. 

```
Raw data (10s):     [45.2] [45.3] [45.1] [45.4] [45.0] [45.5] ... (8,640 points/day)
1-min rollup:       [min:45.0, max:45.5, avg:45.25, count:6] ... (1,440 points/day)
1-hour rollup:      [min:44.1, max:47.2, avg:45.8, count:360] ... (24 points/day)
```

Say in the above, we are averaging the raw data rolling up the sections in order to allow faster queries, these pre-aggregated data allows the query to answer the request without touching raw data. These rollups happen in the background.

##### Block level metadata

Time series databases store some metadata of data blocks mainly in the form of min/max timestamps or min/max values. Say a query looks for 10% CPU usage , block level metadata tells that the query only has 0-5%, so the query is returned without any further search.

##### Putting it all together

Time series databases store data points in the form of
- Measurements, Tags, field and timestamps

```
cpu_usage,host=server-1,region=us-west value=45.2 1699999200000000000
└─────────────────────────────────────┘ └────────┘ └─────────────────┘
        measurement + tags               field          timestamp        
```

Field is some value we would want to store and tags are data points that we can use to filter like host, region etc.

![Screenshot_2025-12-22_at_5.35.39_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2025-12-22_at_5.35.39_PM.png)

Series blocks have sorted data (done in memory before flushing), we use indexes to look for the correct block when a query is made to fetch the correct data. 

```
Query: region='us-west' AND env='prod'

Step 1: Consult the tag index
         region=us-west → [Series 1, Series 2]
         env=prod       → [Series 1, Series 2, Series 3]
         
Step 2: Intersect the sets
         [Series 1, Series 2] ∩ [Series 1, Series 2, Series 3] 
         = [Series 1, Series 2]
         
Step 3: Look up block locations in file index
         Series 1 → Block 0
         Series 2 → Block 1
         
Step 4: Read only blocks 0 and 1 from disk (skip blocks 2, 3!)
         Block 0: timestamps [1700000000, 1700000010], values [45.2, 47.1]
         Block 1: timestamps [1700000000, 1700000010], values [62.3, 61.8]
         
Step 5: Apply time filter (all points match in this case)
         
Step 6: Compute aggregation
         mean([45.2, 47.1, 62.3, 61.8]) = 54.1
```

The tag index let us identify matching series without scanning any data. We read exactly 2 blocks from disk, skipping the 2 blocks for us-east servers entirely. The data within each block was already organized by series, so no sorting or filtering within blocks was needed.

##### Breaking things

A problem here is the Cardinality problem. Cardinality refers to the number of unique tag combinations. Say for metric storage, 1000 hosts with 50 metric will have 50000 series (series are blocks segregated by unique tags) but for a case where the cardinality is super high say using user_id as tags, it would actually slow things down since time series db need to store and sort the series in memory , with so much data accumulated in-mem and in disk queries would be slower that general purpose databases; so user_ids can't be stored as tags but in fields. 

A crucial point that time series databases emphasize on is designing systems understanding the data(lower cardinality tags, higher regular data) and if we can make correct assumptions to better exploit the properties of the system to achieve maximum performance; if the assumptions are violated, the system looses all its benefits and it becomes worse than the general purpose db 
##### Reference

[Hello Interview](https://www.hellointerview.com/learn/system-design/deep-dives/time-series-databases#time-based-partitioning-sharding-by-time)
