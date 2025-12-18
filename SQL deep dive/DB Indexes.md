**Why indexes ?**

Without an index the database needs to look through all the relevant rows to find the target row which is not ideal and will not be performant for large datasets.

Indexes are separate data structure thats stores copy of part of our main table and also stores a reference to point back to main table so as to get the complete data.
Thats why its said that indexes are expensive.
Its important to know that we can create as many indexes as we want but also as few as we can get away with.

Just like the schema is driver by the data , the indexes are driven by queries or the access patterns.

##### B+ Trees

Indexes are represented as B+ Trees as below.

![Screenshot_2024-03-17_at_9.18.50_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2024-03-17_at_9.18.50_PM.png)

Suppose we want to search for a name `Suzanne` , we start with the root node and compare that with the name we searching , if its < node we go left , if its >= node, we go right.

Here we first to right , then we go left and then we go right and find the target.
So indexes are basically skipping the leaf nodes and get to target much faster.

##### Primary Keys

![Screenshot_2024-03-17_at_9.37.44_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2024-03-17_at_9.37.44_PM.png)

As we can see the the column was declared `NOT NULL` by the database even though we did not specify that. Also its a unique column since it acts as a identifier for the row of the table.
The primary keys should be set as `unsigned` to save some space since primary keys should always start from 0 and go on.

**Why primary keys are so important ?**

![Screenshot_2024-03-17_at_9.47.40_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2024-03-17_at_9.47.40_PM.png)

The primary key is basically your entire table. The leaf nodes of the B+ Tree of a primary key index stores all the data of that row. Thats why primary key searches are so quick and we only get one primary key.
So we can say a table is basically an index. Its called clustered index and in SQL dbs its the primary key.

In case if you create a table without a primary key, SQL is going to create one for you and keep track of it under the hood. We can't see that though in the indexes.

##### Secondary Keys

Suppose we have a table as below

![Screenshot_2024-03-25_at_11.11.48_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2024-03-25_at_11.11.48_PM.png)

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

Another way that SQL uses is the selectivity of an index. We define like below

```sql
select count(distinct birthday) from people/ select count(*) from people
select count(distinct state) from people/ select count(*) from people
```

So selectivity is kind of a measure of which index is best to select. So if the number of unique birthdays are higher then number of unique states , its the best index to pick if the query is something where its comparing the both in `WHERE`.
So we can say its calculated by dividing the **_Cardinality_** with total count.
`id` would the col with highest selectivity and if it has an index on it (PK) it would be the best index to pick.

So while trying to decide whether to put index on a col , checking the selectivity of that col would be a good path to follow.

##### Prefix Indexes

Prefix indexes refers to the indexes where we index a part of the value of a row. Suppose we have really long strings like urls, hashes, ulids etc, we index only the prefix of the value to make the index smaller and use that prefix to let the database filter out the ones that match the prefix and then remove that ones that don't match with the given data. So first filter by prefix and then filter by full string.

![Screenshot_2024-03-31_at_8.32.27_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2024-03-31_at_8.32.27_PM.png)

So from the above picture in line 3, we can see how we choose to index the first x characters of the value, 5 in this case.

_How many chars to index though ?_

![Screenshot_2024-03-31_at_8.38.25_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2024-03-31_at_8.38.25_PM.png)

So as we can see we are checking the selectivity of the `x` number of chars. Here we can see with 6 chars we are very close the original selectivity , which is the entire name.
One thing to note that prefix indexes cannot be used to sort. So we cannot do order by or group by.

#### Composite indexes

Composite indexes are single index on multiple columns. Composite indexes can be created by

```sql
alter table <table_name> add index multi(col_1, col_2)
```

There are certain rules of using composite indexes. Lets look at them !

**It cannot skip columns and must follow the order , left to right no skipping.**

Lets say we have an index on first_name, last_name and birthday.

![Screenshot_2024-04-14_at_12.43.21_AM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2024-04-14_at_12.43.21_AM.png)

In the above if we see , the key_len is 202 bytes. key_len tells how much of the index the query is able to use , here is 404 because its using the entire first name part and last name part.

![Screenshot_2024-04-14_at_12.45.59_AM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2024-04-14_at_12.45.59_AM.png)

But in this example its using no index , because we are skipping the order in query. Similarly if we have a query where we have first name & birthday , key_len will be 202 because it can only use `first_name` not `birthday` as it cannot skip the order.

**It stops at the first range condition**

![Screenshot_2024-04-14_at_12.51.59_AM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2024-04-14_at_12.51.59_AM.png)

Here if we see even after not skipping any cols we are still only using a part of the index. Its happening because of the range we have specified for the last name. Its stops because when we have a range we need to scan all the leaf nodes of B-Tree causing us to loose the ability to look further.

How we should choose to build our composite indexes are highly coupled with the access patterns. Another thing to note is we should put commonly used cols at the start and try putting ranges later because it stops at the range as we saw above.

#### Covering Index

An index that covers everything that a query needs , the columns the query is selecting , filtering , searching on. Its not a new index in itself, its more of a representation of an index that covers all the needs of a query. Having a covering index means a secondary index doesn't have to hope back to clustered index (primary key) to get the details because it already has all the data it needs.
How ?
We are only fetching the cols we created our index on so no need to hope back to clustered index for details, the secondary indexes already have everything we need.

e.g. A composite index as we saw above can be an example of covering index if we fetch the cols that are already indexed.

**Covering Index**
In the Column `Extra`, it says `using index` since we are only fetching cols that are indexed. So a covering index case

![Screenshot_2024-05-03_at_12.09.31_AM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2024-05-03_at_12.09.31_AM.png)

In the Column `Extra`, it says `null` since we are only fetching cols that are indexed. So not a covering index.

![Screenshot_2024-05-03_at_12.10.42_AM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2024-05-03_at_12.10.42_AM.png)

But if we add id here , which is a primary index, its still a covering index since its also not referring to a different data structure to fetch details.

#### Functional Indexes

Putting functions on a columns nullifies the indexes as we can see in the below example. This can happen while orms are driving the query generations.

![Screenshot_2024-05-04_at_9.50.29_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2024-05-04_at_9.50.29_PM.png)

So to solve this we can use a function based index.

```sql
alter table add index m(year(created_at))
```

Here we created an index m on this following expression. So running this above query will use the index.

#### Indexing JSON Columns

![Screenshot_2024-05-04_at_10.59.10_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2024-05-04_at_10.59.10_PM.png)

So in-order to index a json field we need generated columns. As we can see above, the email column is used as an index. In the where clause we can also use the generated column name we specified.

The other way could to use functional indexes. But if we see below creating functional indexes using casting does not work because of different collation.

![Screenshot_2024-05-04_at_11.13.30_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2024-05-04_at_11.13.30_PM.png)

So we need to explicitly collate to `utf8m4_bin` as `COLLATE utf8m4_bin` added to query. Underlying MYSQL actually generates a generated column underneath it so both are equally performant.

#### Indexing for wild card searches

![Screenshot_2024-05-04_at_11.21.24_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2024-05-04_at_11.21.24_PM.png)

So we can see for a wild card searches like this where we can searching beginning , indexes does get used. The general rule is that the indexes can get used up until it reaches wildcard, basically we can use an index to find specific data up to a certain point. In here its `like` upto `aaron`.

But for cases like below where we are looking anywhere `like %aaron%` or for the end part `like %aaron`, we cannot use index.

![Screenshot_2024-05-04_at_11.30.50_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2024-05-04_at_11.30.50_PM.png)

We can use generated columns to store reverse of the string or just the domain part depending on use cases.

#### Fulltext Indexes

While simple string searches can help find basic results, what happens when you're searching across multiple columns or trying to find specific words within a block of text? That's where full-text indexing and full-text searching come in handy in databases like MySQL.

To add a full-text index to a table in MySQL, you can use an ALTER TABLE statement. In this example, we'll be adding a full-text index across the `first_name`, `last_name`, and `bio` columns in our `people` table.

```sql
ALTER TABLE people ADD FULLTEXT INDEX `fulltext`(first_name, last_name, bio);
```

![Screenshot_2024-05-26_at_5.47.50_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2024-05-26_at_5.47.50_PM.png)

```sql
SELECT * FROM people WHERE MATCH(first_name, last_name, bio) AGAINST('Aaron');
```

This query will search across all three indexed columns and display all rows where "Aaron" appeared.

For more advanced full-text searches, you can switch to boolean mode. Boolean mode allows you to use modifiers, like `+`, `-`, `>`, `<`, and parentheses in your search query.

Here's an example of a boolean search query:

```sql
SELECT * FROM people
  WHERE MATCH(first_name, last_name, bio) AGAINST('+Aaron -Francis' IN BOOLEAN MODE);
```

This query will search for all rows where "Aaron" appears and exclude any rows where "Francis" appears. The `+` indicates that "Aaron" is a required search term, and the `-` indicates that "Francis" is excluded.

In boolean mode, you can also add quotation marks to search for an exact phrase or use the `NEAR` operator to search for words within a certain distance of each other.

#### Foreign Keys

Foreign keys are used to refer to the table the table with the foreign key is connected with. There is another thing called Foreign key constraint which basically maintain the referential integrity between tables. It helps maintain that all data references are valid and consistent.

```sql
CREATE TABLE parent (
  ID BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY
);
```

This creates a table `parent` with a single column `id` as a primary key. Now let's create the `child` table with a foreign key constraint that references the `parent` table:

```sql
CREATE TABLE child (
  ID BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  parent_id BIGINT UNSIGNED,

  FOREIGN KEY (parent_id) REFERENCES parent(ID)
);
```

The type of foreign key column should be exactly same as the parent column.

![Screenshot_2024-05-26_at_6.04.03_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2024-05-26_at_6.04.03_PM.png)

We can see an index was created on `parent_id` with some constraints. When something is inserted into child table it checks for the foreign key in parent table to see if that exists , if not it throws an error.

Also trying to delete from parent without deleting the child , it throws an error. It order to delete the children as well we need to add some options to the table called `on delete cascade`.

But doing this cause issues , since it might end up trying to delete a lot of child and at scale it could be a huge number. So we need to be careful on how we implement the delete part.
