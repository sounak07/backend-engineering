## Database Queries

##### `EXPLAIN` 

**Postgres**

```sql
-- create
CREATE TABLE EMPLOYEE (
  empId INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  dept TEXT NOT NULL
);

-- insert
INSERT INTO EMPLOYEE VALUES (0001, 'Clark', 'Sales');
INSERT INTO EMPLOYEE VALUES (0002, 'Dave', 'Accounting');
INSERT INTO EMPLOYEE VALUES (0003, 'Ava', 'Sales');

CREATE INDEX dpt_idx ON EMPLOYEE (dept);

-- fetch 
SET enable_seqscan TO off;
explain (FORMAT JSON) SELECT * FROM EMPLOYEE WHERE dept = 'Sales';
```

The Explain for a pg database
```json
[                                           +
   {                                         +
     "Plan": {                               +
       "Node Type": "Index Scan",            +
       "Parallel Aware": false,              +
       "Async Capable": false,               +
       "Scan Direction": "Forward",          +
       "Index Name": "dpt_idx",              +
       "Relation Name": "employee",          +
       "Alias": "employee",                  +
       "Startup Cost": 0.13,                 +
       "Total Cost": 8.15,                   +
       "Plan Rows": 1,                       +
       "Plan Width": 68,                     +
       "Index Cond": "(dept = 'Sales'::text)"+
     }                                       +
   }                                         +
 ]
```

We can its using Index Scan and also specifies which index its using

**MYSQL**

![alt text](/resources/Screenshot%202024-05-30%20at%208.27.11%20PM.png)

- **ID**: A unique identifier for the query being executed.
- **Select Type**: Tells us the type of select statement is being executed. This can be simple, primary, union, or a few others.
- **Table**: The name of the table being accessed.
- **Partitions**: Displays the partitions being accessed for the query (beyond the scope of this course).
- **Type**: The kind of access MySQL used to retrieve the data. This is one of the most important column values, and we'll discuss it in more detail later.
- **Possible Keys**: The possible indexes that MySQL could use.
- **Key**: The actual index that MySQL uses.
- **Key Length**: Displays the length of the index used by MySQL.
- **Ref**: The value being compared to the index. In above case both are const.
- **Rows**: An estimated number of rows that MySQL needs to examine to return the result.
- **Filtered**: The estimated percentage of rows that match the query criteria.


**The Type column**

[Const](https://planetscale.com/learn/courses/mysql-for-developers/queries/explain-access-types?autoplay=1#const)

At the top of the list, the `const` access method is one of the most efficient. `Const` access is only used when a primary key or unique index is in place, allowing MySQL to locate the necessary row with a single operation. When you see `const` in the type column, it's telling you that MySQL knows there is only one match for this query, making the operation as efficient as possible.

[Ref](https://planetscale.com/learn/courses/mysql-for-developers/queries/explain-access-types?autoplay=1#ref)

The `ref` access method is slightly less efficient than `const`, but still an excellent choice if the right index is in place. `Ref` access is used when the query includes an indexed column that is being matched by an equality operator. If MySQL can locate the necessary rows based on the index, it can avoid scanning the entire table, speeding up the query considerably.

[Fulltext](https://planetscale.com/learn/courses/mysql-for-developers/queries/explain-access-types?autoplay=1#fulltext)

MySQL provides an option to create full-text indexes on columns intended for text-based search queries. The `fulltext` access method is used when a full-text index is in place and the query includes a full-text search. `Fulltext` access allows MySQL to search the index and return the results quickly.

[Range](https://planetscale.com/learn/courses/mysql-for-developers/queries/explain-access-types?autoplay=1#range)

When you use `range` in the where clause, MySQL knows that it will need to look through a range of values to find the right data. MySQL will use the B-Tree index to traverse from the top of the tree down to the first value of the range. From there, MySQL consults the linked list at the bottom of the tree to find the rows with values in the desired range. It's essential to note that MySQL will examine every element in the range until a mismatch is found, so this can be slower than some of the other methods mentioned so far.

[Index](https://planetscale.com/learn/courses/mysql-for-developers/queries/explain-access-types?autoplay=1#index)

The `index` access method indicates that MySQL is scanning the _entire_ index to locate the necessary data. `Index` access is the slowest access method listed so far, but it is still faster than scanning the entire table. When MySQL cannot use a primary or unique index, it will use `index` access if an index is available.

```sql
-- Create the EMPLOYEE table
CREATE TABLE EMPLOYEE (
  empId INT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  dept VARCHAR(100) NOT NULL
);

-- Insert data into the EMPLOYEE table
INSERT INTO EMPLOYEE (empId, name, dept) VALUES (1, 'Clark', 'Engineering');
INSERT INTO EMPLOYEE (empId, name, dept) VALUES (2, 'Dave', 'Accounting');
INSERT INTO EMPLOYEE (empId, name, dept) VALUES (3, 'Ava', 'Sales');

-- Add an index on the dept column
CREATE INDEX dept_idx ON EMPLOYEE (dept);

-- Verify the index
SHOW INDEX FROM EMPLOYEE;

-- Explain plan to check index usage
EXPLAIN SELECT dept FROM EMPLOYEE WHERE dept != 'Sales';
```

Here it will look the entire index since it can't compare the value with a node and decide which way to go, it needs to scan the entire index until it finds something thats not `Sales` 

[All](https://planetscale.com/learn/courses/mysql-for-developers/queries/explain-access-types?autoplay=1#all)

Finally, the `all` access method means that MySQL is scanning the entire table to locate the necessary data. `All` is the slowest and least efficient access method, so it's one that you want to avoid as much as possible. MySQL may choose to scan the entire table when there is no suitable index, so this is an excellent opportunity to audit your indexing strategy. There might be an index present but when MySQL sees that it will return so many ids that it would anyway have to refer to the main table to select the rows(considering that its selecting rows that are not indexed), it would just skip index all together. 

```json
-- Create the EMPLOYEE table
CREATE TABLE EMPLOYEE (
  empId INT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  dept VARCHAR(100) NOT NULL
);

-- Insert data into the EMPLOYEE table
INSERT INTO EMPLOYEE (empId, name, dept) VALUES (1, 'Clark', 'Engineering');
INSERT INTO EMPLOYEE (empId, name, dept) VALUES (2, 'Dave', 'Accounting');
INSERT INTO EMPLOYEE (empId, name, dept) VALUES (3, 'Ava', 'Sales');

-- Add an index on the dept column
CREATE INDEX dept_idx ON EMPLOYEE (dept);

-- Verify the index
SHOW INDEX FROM EMPLOYEE;

-- Explain plan to check index usage
EXPLAIN SELECT dept FROM EMPLOYEE WHERE empId > 1 (1);
EXPLAIN SELECT dept FROM EMPLOYEE WHERE empId > 2 (2);
```

This above query(1) will use ref = 'index' but query(2) will use ref = 'range'. Interesting !

**Why the Difference?**
- **Empirical Data**: With `empId > 1`, the database engine sees that a small number of rows will be returned and uses an index lookup.
- With `empId > 3`, it anticipates a range of values to be scanned (even if it's empty), and thus it uses a range scan.

But if the number of rows are more then 3, it wont use index anymore for query(1), since it needs to scan a huge range.

#### `EXPLAIN ANALYZE`

`EXPLAIN ANALYZE` actually runs the query and provides detailed statistics on the query's execution plan. **It's important to note that this format actually runs the query**, so it should be used with caution.

```sql
-- Create the EMPLOYEE table
CREATE TABLE EMPLOYEE (
  empId INT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  dept VARCHAR(100) NOT NULL
);

-- Insert data into the EMPLOYEE table
INSERT INTO EMPLOYEE (empId, name, dept) VALUES (1, 'Clark', 'Engineering');
INSERT INTO EMPLOYEE (empId, name, dept) VALUES (2, 'Dave', 'Accounting');
INSERT INTO EMPLOYEE (empId, name, dept) VALUES (3, 'Ava', 'Sales');
INSERT INTO EMPLOYEE (empId, name, dept) VALUES (4, 'Ava', 'Sales');
INSERT INTO EMPLOYEE (empId, name, dept) VALUES (5, 'Ava', 'Sales');
INSERT INTO EMPLOYEE (empId, name, dept) VALUES (6, 'Ava', 'Sales');


-- Add an index on the dept column
CREATE INDEX dept_idx ON EMPLOYEE (dept);

-- Verify the index
SHOW INDEX FROM EMPLOYEE;

-- Explain plan to check index usage
EXPLAIN analyze SELECT dept FROM EMPLOYEE WHERE empId > 2;

```

```bash
-> Filter: (employee.empId > 2)  (cost=1.06 rows=4) (actual time=0.009..0.012 rows=4 loops=1)
    -> Index range scan on EMPLOYEE using PRIMARY  (cost=1.06 rows=4) (actual time=0.009..0.011 rows=4 loops=1)

```

This gives a more detailed analysis in a tree format with params like 
`cost` is the estimated total cost to retrieve all rows matching the query. It includes both the startup cost and the cost to retrieve all the rows.

`rows` is the number of rows that will be retrieved by this part of the execution plan. Here its 4 for obvious reasons. 

- Actual Time (`actual time=0.009..0.012`):
    - This shows the actual time taken to perform this part of the execution plan.
    - The two numbers indicate the range from the start to the end of this step. For example, it took 0.009 milliseconds to start returning rows and 0.012 milliseconds to complete returning rows.
- Loops (`loops=1`):
    - This indicates how many times this(the data retrieve part) part of the plan was executed. In this case, it was executed once.

#### Index obfuscation

It refers to a case when we miss out on using index on a query due to some modifications done on the value while comparing. 

For example, instead of this:

```sql
SELECT * FROM film WHERE length / 60 < 2;
```

We should write it like this:

```sql
SELECT * FROM film WHERE length < 2 * 60;
```

Here we are avoiding changing values of length to be able to use index.

#### Redundant and approximate conditions

Cases where redundant conditions can actually be used to avoid index obfuscation. 
Suppose we have todos table and a row `due_date` and `due_time` but only the `due_date` is indexed. 

```sql
SELECT * FROM todos
  WHERE
  ADDTIME(due_date, due_time) BETWEEN NOW() AND NOW() + INTERVAL 1 DAY
  AND
  due_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL 1 DAY
```

The above example demonstrates how we can use a redundant condition to avoid index obfuscation.

#### Select only what you need

Selecting only what we need is important because there is no point fetching data that we are not gonna use, specially for large data columns like `TEXT`, `JSON` etc since they are actually physically stored in a different place then all the other data.

But limiting selects could be an issue for a case where unintentionally we are trying to select a column  that was never pulled out of database. 

```python

person = query("Select name, position from people")

if person.is_admin is None:
	## do something
```

The `is_admin` will always be null because it was never pulled out of database. So it could led to several unexpected issues.

One of the ways to do `select *` and also avoid pulling out large columns is by declaring the column as `invisible`. In this way, we would never fetch unless its explicitly specified as `select *, col_name from table_name`

#### Limiting rows

![alt text](/resources/Screenshot%202024-06-02%20at%209.52.27%20PM.png)

`count(*)` uses the smallest secondary index to count the number of rows since the primary index scanning will be slower because of the presence of all the data there which make the reading from the disk slower the leaf nodes will also be far from each other because of more data in them.

```sql
select count(id) from people 
```

Even this will also do the same. One thing to note we only need to specify the column name if we are trying to count the none null values of that specified column. 
Same principle applies to `avg`, `sum`, `DISTINCT` etc.

```sql
select * from people LIMIT 10 offset 20
```

Its a way to limit the number of records that are being returned.  The above query will return 10 after offsetting the first 20 columns. 

```sql
select * from people LIMIT 10 offset 20 orderby id
```
Note that Ordering the limits is a good way to order the results in your way otherwise mysql decides on how to order.

#### Joins Overview

Indexes in joins are very important to optimise the overall query otherwise we might end up scanning 1000s of rows just to join a few tables.

With Index
```bash
-> Nested loop left join  (cost=29.42 rows=55)
    -> Nested loop left join  (cost=10.25 rows=55)
        -> Filter: (film.id <= 10)  (cost=2.82 rows=10)
            -> Index range scan on film using PRIMARY  (cost=2.82 rows=10)
        -> Covering index lookup on film_actor using idx_fk_film_id (film_id=film.id)  (cost=1.06 rows=5)
    -> Single-row index lookup on actor using PRIMARY (id=film_actor.actor_id)  (cost=0.84 rows=1)
```

Without Index
```bash
-> Nested loop left join  (cost=12347.65 rows=54620)
    -> Left hash join (film_actor.film_id = film.id)  (cost=5519.98 rows=54620)
        -> Filter: (film.id <= 10)  (cost=3.02 rows=10)
            -> Index range scan on film using PRIMARY  (cost=3.02 rows=10)
        -> Hash
            -> Index scan on film_actor using PRIMARY  (cost=54.93 rows=5462)
    -> Single-row index lookup on actor using PRIMARY (id=film_actor.actor_id)  (cost=0.08 rows=1)
```

If we see the cost has increased multiple folds and the number of rows scanned have increased significantly. 

#### Subquery 

In MySQL, subqueries allow you to run a separate query inside your main query, and they can be super powerful in situations where joins might not work exactly as you want them to.

The subquery is not something where we run the queries separately and then put the data in the main query, we want the subquery to run and compute the logic on the go with the same overall query. 

```sql
SELECT * FROM customer
WHERE
  id IN (
    SELECT customer_id FROM payment WHERE amount > 5.99
  );
```

#### Common table expressions (CTEs)

At their core, a Common Table Expression is a SQL statement that can be referenced within the context of a larger query. CTEs are supported in MySQL 8. CTEs allow queries to be broken down into smaller parts that can be more easily comprehended by us mere humans. By doing so, it becomes simpler to reason about and compose complex queries.

The `WITH` keyword is followed by the name of the CTE and the query that generates it in parentheses. After defining the CTE, we can reference it in another query. Here's an example that uses CTEs to find customers who have spent more than the average on purchases at a particular store:

```sql
with spend_last_6 as (
  select
    customer_id,
    sum(amount) as total_spend
  from
    payment
    inner join customer on customer.id = payment.customer_id
  where
    store_id = 1
    and payment_date > CURRENT_DATE - INTERVAL 6 MONTH
  group by
    cusomter_id
)

select * from spend_last_6 where total_spend > (
	select avg(total_spend) from spend_last_6
)
```

As we can see we are referring the CTE multiple times to derive more data or a different kind of data from that. 
They very useful OLAP systems.

#### Recursive CTE

Let's look at an example of how to use a Recursive CTE to build a simple list of numbers in SQL. We'll create a table called "numbers" and define our Recursive CTE to generate a sequence of numbers from 1 to 10.

Basically a way to create and append to table and use the same table again while certain conditions are met.

```sql
WITH RECURSIVE numbers AS (
  SELECT 1 AS n -- Initial Condition
  UNION ALL
  SELECT n + 1 FROM numbers WHERE n < 10 -- Recursive Condition
)

SELECT * FROM numbers;
```

Here's what's happening in this code:

- We define a CTE called `numbers` using the WITH keyword and specify the `RECURSIVE` modifier.
- We define our initial condition, which selects the number 1 and assigns it the alias `n`.
- We define our recursive condition, which selects the value of n + 1 from the table `numbers`. This incrementally generates the sequence of numbers from 1 to 10.

If we run this code, we get a list of numbers from 1 to 10.


#### Union

A UNION query is used to combine the results of two or more SELECT statements into a single result set. Specifically, it takes the values from one table or query, and instead of putting them side-by-side with another table or another query, it puts them together over-under.

```sql
SELECT
  first_name,
  last_name,
  email_address
FROM customers

UNION ALL

SELECT
  first_name,
  last_name,
  email_address
FROM staff;
```

Notice that we use `UNION ALL` instead of `UNION` to prevent MySQL from eliminating duplicate rows, which can be computationally expensive when we have a large result set. Instead, we simply combine the result sets, knowing that duplicates may exist.

#### Sorting and Limiting

Sorting your rows is not free. It can take a significant amount of resources and time to sort large data sets, and thus, it's important to do it with caution. If you don't need your rows in a certain order, don't order them.

However, if you need to order your rows, it's essential to do it efficiently and effectively. In order to optimize your queries, we must understand how to use indexes to make sorting cheaper.

`ORDER BY` basically sorts the data in order, default sort is ascending unless otherwise specified. 

Order of the returned rows can be different in different types if the column thats being sorted is not deterministic enough so MySQL gets to decide the order. 

To avoid this we can add something thats always unique like the id (Primary key).

```sql
SELECT id, birthday FROM people ORDER BY birthday, id;
```

Suppose we want to skip the first 10 rows and get the next may be 100 rows by limiting.

```sql
SELECT id, birthday FROM people ORDER BY birthday, id LIMIT 100 OFFSET 20;
```

But this comes with a cost, while ordering MySQL needs to order(sort) all of them(120 rows) and then throw away the first 20 rows and return the next 100 which is inefficient. 

#### Sorting with Indexes

We will begin by ordering the results of the people table by birthday and using a limit of 10.

```sql
SELECT
  *
FROM
  people
ORDER BY
  birthday ASC
LIMIT
  10;
```

When we run this query and examine it using the EXPLAIN statement, we see that it employs the "using file sort" method. This means that MySQL produced a sorted result by sorting all the results, not by reading an index in order.

| id  | select_type | table  | type | possible_keys | key | key_len | ref | rows   | filtered | Extra          |
| --- | ----------- | ------ | ---- | ------------- | --- | ------- | --- | ------ | -------- | -------------- |
| 1   | SIMPLE      | people | ALL  |               |     |         |     | 491583 | 100.00   | Using filesort |

To ensure its efficient we need to use indexing on the ordered column , the analyze results below is making this clear. 

We can see in case there is no index , it scans the entire table which is very costly.

![alt text](/resources/Screenshot%202024-06-30%20at%2011.07.30%20AM.png)


```sql
SELECT
  *
FROM
  people
ORDER BY
  birthday ASC, ID ASC
LIMIT
  10;
```

In this case, MySQL can still use the birthday index, even though there is another column involved in the sorting process. 
Its because secondary indexes has a reference to the primary key so it knows what the primary key and is able to append that easily. 

#### Backward index scans

In MySQL 8.0 or later, we can perform backward index scans when sorting in descending order.

For example, if we set the birthday index to order in descending order and rerun the query, we can see that MySQL performs a backward index scan(Check extras in explain table). This is a new optimization that MySQL uses when it is able to read an index in reverse order.

```sql
SELECT
  *
FROM
  people
ORDER BY
  birthday DESC
LIMIT
  10;
```

But if DESC is something we always want we should create a backend index as there is a 15% penalty here.

```sql
ALTER table <table_name> add INDEX (birthday desc)
```

#### Sorting with Composite index

Suppose we have a composite index 

```sql
ALTER TABLE people ADD INDEX composite_idx(first_name, last_name, birthday);
```

Now if we want to use this index to order rows, we have make sure we follow the rules of using composite index.

```sql
SELECT
 *
FROM
  people
ORDER BY
  first_name
LIMIT 10;
```

We should see that the query executes without any file sorting. This is because the multi-column index allows the database to efficiently sort and retrieve the requested data.

Let's say we want to sort by `last_name` but skip over `first_name`. According to our rules, this is not allowed. However, we can unlock the `last_name` key part for sorting by adding an equality condition on the `first_name` column. Here's the query:

```sql
SELECT
  *
FROM
  people
WHERE
  first_name = 'John'
ORDER BY
  last_name;
```

Here if we remove the first_name equality we will end up not using the index. 
```sql
SELECT
  *
FROM
  people
WHERE
  first_name = 'John'
ORDER BY
  birthday;
```

Similarly in the above query, we will end up not using the index but that again changes if we add the last_name as equality or in the order by.

**Sorting Direction**

```sql
SELECT
  *
FROM
  people
ORDER BY
  first_name asc;
```

Here we will use the index, but if we do 

```sql
SELECT
  *
FROM
  people
ORDER BY
  first_name asc , last_name desc;
```
 
 It will use the file sort. Index can only be used in order, basically while ordering we need to ensure what order we created our index in, is the order of the sort, if we need a different order we ensure we have a index in that order.
So in order to efficient use the above query , we can create an index as

```sql
ALTER TABLE people ADD INDEX composite_idx(first_name asc, last_name desc, birthday)
```

#### Dealing NULLs

When dealing with null values in SQL, one of the first things to consider is how to compare null values. In MySQL, null is not equal to anything, including itself. For example, if we run the query `select null = null` we’ll get `null` back as the result.

Similarly, if we use the equals operator to compare a column with a null value, we’ll also get null back as the result. For example, if we run the query `select null = one` we’ll get `null` back as the result.

To account for null values, we can use the null-safe equal operator `<=>`, also known as the “spaceship operator.” This operator considers null and another null value as equal.

![alt text](/resources/Screenshot%202024-06-30%20at%2012.28.03%20PM.png)


Here we can see that we are getting both rows because now null is considered equality , basically now even if language_id is null , it will be considered as we used `<=>`.  But `=` rejects those causes because `null = null` returns a null and its not considered. 

To compare a column with a null value, we can use the `is null` or `is not null` operators. These operators will return true or false, depending on whether the value is null or not null.

![alt text](/resources/Screenshot%202024-06-30%20at%2012.20.58%20PM.png)

Coalesce is a function thats selects the first null value. The coalesce of null, 8, null , 1 is 8. 

![alt text](/resources/Screenshot%202024-06-30%20at%2012.23.41%20PM.png)



[Reference](https://planetscale.com/learn/courses/mysql-for-developers/queries)