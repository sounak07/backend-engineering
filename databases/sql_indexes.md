**Why indexes ?**
Without an index the database needs to look through all the relevant rows to find the target row which is not ideal and will not be performant for large datasets.

Indexes are separate data structure thats stores copy of part of our main table and also stores a reference to point back to main table so as to get the complete data. 
Thats why its said that indexes are expensive.
Its important to know that we can create as many indexes as we want but also as few as we can get away with. 

Just like the schema is driver by the data , the indexes are driven by queries or the access patterns. 

#### B+ Trees

Indexes are represented as B+ Trees as below.

![alt text](/resources/Screenshot%202024-03-17%20at%209.18.50%20PM.png)

Suppose we want to search for a name `Suzanne` , we start with the root node and compare that with the name we searching , if its < node we go left , if its >= node, we go right.

Here we first to right , then we go left and then we go right and find the target.
So indexes are basically skipping the leaf nodes and get to target much faster. 


#### Primary Keys

![alt text](/resources/Screenshot%202024-03-17%20at%209.37.44%20PM.png)

As we can see the the column was declared `NOT NULL` by the database even though we did not specify that. Also its a unique column since it acts as a identifier for the row of the table.
The primary keys should be set as `unsigned` to save some space since primary keys should always start from 0 and go on. 

**Why primary keys are so important ?**

![alt text](/resources/Screenshot%202024-03-17%20at%209.47.40%20PM.png)

The primary key is basically your entire table. The leaf nodes of the B+ Tree of a primary key index stores all the data of that row. Thats why primary key searches are so quick and we only get one primary key. 
So we can say a table is basically an index. Its called clustered index and in SQL dbs its the primary key. 

In case if you create a table without a primary key, SQL is going to create one for you and keep track of it under the hood. We can't see that though in the indexes. 


##### Secondary Keys

Suppose we have a table as below 

![[Screenshot 2024-03-25 at 11.11.48 PM.png]]

Now we add name and secondary key(index it) and we try to find Zoe. Now we will follow the B+ Tree structure to find the name. But at this point we want the id and email so what now ? 
The secondary key B Tree+ leaf node actually stores the pointer back to primary key. As we know every leaf node of primary index tree contains all the data of the table so we got our data. 

One thing to note is primary key index is a copy of part of data so it can only point back to the primary key if that row was indexed. 
##### Primary Key data types

Recommended type is obviously unsigned big int since they are compact.

So what about strings as PK like uuid, guid etc ?
Sure they can also be used but there are certain trade-offs. Since secondary key indexes store primary key pointer carrying around a long string is something we need to think about. 
Also incase of auto incrementing keys the row gets inserted at the bottom as a sorted manner but for uuid it might not be the case so the B+ Tree needs to be balanced every time a new row is inserted so sorted uuids could be viable option we can go with. 

##### Where to add indexes

It depends on the query and access pattern. Indexes are useful for various types of queries like direct match, range , bounded and unbounded ranges, in ordering and even for grouping. 

We can verify that by running an explain on the query and check what are the possible keys the query is considering. Possible keys indicates the cols the query can use to fasten the process.

##### Index Selectivity 

Suppose there are 2 indexes in a table and in a query we specify `WHERE` with both of them , SQL engine can only use one key and it chooses the key based on the number of distinct values , basically something that would take longer to find if tried without indexes. 

Another way that SQL uses is the selectivity of an index.  We define like below

```sql
select count(distinct birthday) from people/ select count(*) from people
select count(distinct state) from people/ select count(*) from people
```

So selectivity is kind of a measure of which index is best to select. So if the number of unique birthdays are higher then number of unique states , its the best index to pick if the query is something where its comparing the both in `WHERE`.
So we can say its calculated by dividing the ***Cardinality*** with total count. 
`id` would the col with highest selectivity and if it has an index on it (PK) it would be the best index to pick.

So while trying to decide whether to put index on a col , checking the selectivity of that col would be a good path to follow. 

##### Prefix Indexes

Prefix indexes refers to the indexes where we index a part of the value of a row. Suppose we have really long strings like urls, hashes, ulids etc, we index only the prefix of the value to make the index smaller and use that prefix to let the database filter out the ones that match the prefix and then remove that ones that don't match with the given data. So first filter by prefix and then filter by full string. 

![[Screenshot 2024-03-31 at 8.32.27 PM.png]]

So from the above picture in line 3, we can see how we choose to index the first x characters of the value, 5 in this case.

*How many chars to index though ?*

![[Screenshot 2024-03-31 at 8.38.25 PM.png]]

So as we can see we are checking the selectivity of the `x` number of chars. Here we can see with 6 chars we are very close the original selectivity , which is the entire name.
One thing to note that prefix indexes cannot be used to sort. So we cannot do order by or group by. 

