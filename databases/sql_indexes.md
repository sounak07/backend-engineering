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


