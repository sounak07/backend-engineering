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

