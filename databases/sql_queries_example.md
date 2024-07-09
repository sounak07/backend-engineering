
#### MD5 Column

Suppose we have a column like a huge text or url, we can't index those fields, what we can is we can add a generated column and calculate the MD5 of that column and index that MD5 column instead and use it in our queries. 

![alt text](/resources/Screenshot%202024-06-30%20at%2012.45.55%20PM.png)


To avoid has collision we can also add the url column as a redundant column.

```sql
url_md5('url_value') and url('url_value')
```

To improve this further we can binary string instead of just string. Note that because the MD5 column is a binary column (a string of bytes, not characters), we must use the `UNHEX` function to convert the characters to a binary string.


![alt text](/resources/Screenshot%202024-06-30%20at%2012.49.30%20PM.png)


Also a tip to keep a large data column like text or blob , we can consider making that invisible to allow faster fetch since these type of data is usually stored in a separately and the engine needs to fetch that which is costly.

#### MD5 on multiple Columns

Consider the example of a table that stores normalized addresses. The table consists of four columns – `primary_line`, `secondary_line`, `urbanization`, and `last_line`. The goal is to store unique addresses and only keep the pretty, normalized version of an address. However, since there is no natural ID or other unique identifier, we need to create our unique ID.

**Creating the MD5 hash**

To generate the MD5 hash, we create a new column, simply called MD5. Since the table includes binary 16, we will use that for the MD5 hash column. We can do this by running the following command:

```sql
ALTER TABLE addresses ADD COLUMN md5 BINARY(16) GENERATED ALWAYS AS (
  UNHEX(MD5(
    CONCAT_WS('|', primary_line, secondary_line, urbanization, last line)
  ))
);
```

Note that we are using MD5 hash concatenated with separator (`|`). The first value passed in is the separator. We use the `CONCAT_WS` function to combine all four columns and then generate the MD5 hash. This is necessary to do because we need to as just concatenating the values with rows having `null` will make the entire string go `null` . So we use this separator.

By using this method to create unique MD5 hashes from multiple columns, we can now enforce uniqueness and perform lookups faster than a composite index across multiple character columns. This also saves us from having to maintain a more complex index structure.

Creating an MD5 hash from multiple columns is a powerful tool that can be used in various applications to achieve fast and efficient search results.

#### Bitwise Operations

When designing a database, it is often necessary to store "flags," or true/false values. One way to do this is to create a separate column for each value, but as the number of flags increases, this approach becomes impractical. One solution is to use a JSON column to store all the flags in a single field. However, this approach comes at the cost of increased space usage. We explore an alternative solution that uses a tiny integer column to store multiple bits of information in a single field.

```sql
ALTER TABLE users ADD COLUMN flags TINYINT UNSIGNED DEFAULT 0;
```

Suppose we have a column called flags which is of type `int` .  We would be setting the default value to 0 and making the column `tinyint unsigned` to store only positive integers.

To understand this we need to look into how bits work.

A byte is a unit of digital information that consists of eight bits. A bit is a binary digit that can be either 0 or 1. By manipulating the bits in an integer, we can store multiple flags in a single field.

For example, suppose we have the following eight flags:

1. dark_mode
2. super_admin
3. notification_opt_in
4. metered_billing
5. rollout_chat
6. experiment_blue
7. log_verbose
8. new_legal_disclaimer

We can assign each flag to a bit in the integer column as follows:
![alt text](/resources/Screenshot%202024-07-09%20at%209.58.25%20PM.png)


Using this mapping, we can store up to eight flags in a single byte. To store multiple flags, we need to turn on the corresponding bits.

For example, suppose a user has turned on the `dark_mode` and `rollout_chat` flags. To represent this, we need to turn on bits 1 and 5. Using binary notation, this would look like this: `00010100`.

![alt text](/resources/Screenshot%202024-07-09%20at%209.58.45%20PM.png)

To convert this to an integer value, we can add up the decimal value of each bit that is turned on. In this case, that would be 1 + 16 = 17.

We can store this value, 17, in the `flags` column for this user.

![alt text](/resources/Screenshot%202024-07-09%20at%209.52.08%20PM.png)


to find all users who have both the `dark_mode` and `rollout_chat` flags turned on, we can use the following SQL statement:

```sql
SELECT * FROM users WHERE flags & 17 = 17;
```

In this statement, we use the bitwise AND operator (`&`) to compare the value of the `flags` column with the binary value of 17 (`00010100`), which represents both the `dark_mode` and `rollout_chat` flags. If the result of the bitwise AND operation is 17, it means that both flags are turned on, and we include that user in the result set.

Similarly , we can check if the user has dark mode enabled as

```sql
SELECT * FROM users WHERE flags & 1 = 1;
```

 **Tradeoffs**

Using a tiny integer column to store multiple flags in a single field is an efficient way to save space in the database. However, it comes with some tradeoffs.

- **Reduced readability:** The binary representation of flags in the `flags` column is not human-readable. It can be difficult to interpret the meaning of the flags without consulting a mapping table.
    
- **Limited number of flags:** The number of flags that can be stored in a single byte is limited to eight. If we need to store more flags, we need to use a larger integer column or a JSON column.
    
- **Application logic overhead:** To use the bitwise operators to query the flags, we need to write additional application logic that maps the flags to their corresponding bit values. This can add complexity to the codebase.

#### Timestamps versus Booleans

```sql
CREATE TABLE posts(
  title VARCHAR(125),
  -- ....
  is_archived BOOLEAN
);
```

Initially, we set the "is_archived" column as boolean, which is a useful data type. It allows us to store a true/false value in a single bit, providing an optimal storage solution for storing binary values. However, using timestamps instead of booleans has its benefits too.

**Benefit of using timestamps instead of booleans**

When we change the data type to timestamps, we get access to an extra piece of information. Instead of just storing a boolean value, we get to store an archive timestamp, which tells us when the post was archived.

```sql
CREATE TABLE posts(
  title VARCHAR(125),
  -- ....
  archived_at timestamp null
);
```
With this in place, we can still use the `archived_at` column as if it is a boolean value with the following query:

```sql
SELECT * FROM posts WHERE archived_at IS NULL;
```

This query returns all unarchived posts, which is equivalent to the boolean query

```sql
SELECT * FROM posts WHERE is_archived = false;
```

However, the `archived_at` column provides us with more information, namely the _time_ at which the post was archived, which could be useful in the long run.


#### Claiming rows

Its a case where we add a column to a table and use it to indicate the claim status of the row.

```sql
CREATE TABLE imports (
  id INT NOT NULL AUTO_INCREMENT,
  filename VARCHAR(255),
  owner INT DEFAULT 0,
  available TINYINT DEFAULT 1,
  started_at TIMESTAMP,
  finished_at TIMESTAMP,
  PRIMARY KEY (id),
  INDEX available_owner (available, owner)
);
```

Note that we have included a composite index on the available and owner columns in order to make our queries more efficient.

#### Selecting available rows

Our first step is to select any available rows for our workers to claim. We can do this by running the following query:

```sql
SELECT
  *
FROM
  imports
WHERE
  available = 1
LIMIT 1;
```
This query retrieves the most recent unclaimed row from the table. However, it is important to note that **this method is flawed**, as it does not guarantee that another worker has not already claimed this row by the time our worker updates it.

#### Updating claimed rows

Instead of selecting a row and then updating it, we can issue a blind update that claims the row as soon as it is found. We can do this using the following query:

```sql
UPDATE imports
SET
  owner = 32, -- unique worker id
  available = 0
WHERE
  owner = 0
  AND
  available = 1
LIMIT 1;
```

In this example, we are claiming the row for worker #32 by setting the owner column to 32 and the available column to 0. On your application side, you would need to make sure each worker process has a unique id. We are also only claiming one row at a time with the LIMIT 1 clause.

#### Checking claimed rows

Once a row has been claimed, we can ensure that only the owner of the row is able to modify or process it. We can do this by selecting rows where the owner is equal to the worker ID.

```sql
SELECT
  *
FROM
  imports
WHERE
  owner = 32;
```


#### Meta tables

Case where the table is very long and wide and only a bunch of columns are frequently accessed, we can use something like this. 

To implement this, we implement a short table of 3-4 columns which are frequently accessed and push rest in a meta table.
Whenever rest of the data is needed , we just join the two tables and access it all. 

```sql
SELECT
  *
FROM
  film_narrow
INNER JOIN film_addendum ON film_narrow.id = film_addendum.film_id
```

#### Offset limit pagination 

Before diving into the different methods of pagination, it is important to emphasize the significance of ensuring deterministic ordering. If your ordering is not deterministic, your records may not show up correctly, which can lead to confusion for your users. For pagination to be effective, you must order your records in a stable and deterministic manner.

Let's start by examining the limit offset method. With this method, the first step is to select records from the database. You should then order the records by a field (or multiple fields!) to ensure deterministic ordering. The next step is to specify the page size by using the `LIMIT` keyword followed by the number of records you want to show per page. Finally, you specify the offset by using the `OFFSET` keyword followed by the starting position for the current page.

Here's an example:

```sql
SELECT
  *
FROM
  people
ORDER BY
  birthday,
  id
LIMIT 100
OFFSET 0;
```

In this example, we are selecting all records from the `people` table, ordering by the `birthday` column, and showing 100 records per page. The `OFFSET` is set to 0 because we are on the first page.

**Strengths of limit/offset method**

One significant advantage of the limit offset method is that it is user-friendly and easy to implement. You can create a simple query to construct the pagination, and users can jump directly to the page they want to view by using their desired offset number. This method provides directly addressable pages, so if users want to jump to a certain page, they can do so quickly and easily.

**Drawbacks of limit/offset method**

One significant limitation of limit offset is that the page numbers can drift as you navigate through the records. For example, if a record is deleted from your current page, it may cause a record to shift from the next page to the current page, leading to confusion. Moreover, as you navigate deeper into the records, the method becomes significantly more expensive, meaning the database has to do more work to fetch that specific page.

A trick to avoid doing `count(*)` to count number of records and hence pages, we can actually check if there are extra records than the requested page count, if so we show the next button. But this is useful only if just the presence of next button is sufficient.
#### Cursor Pagination

Cursor-based pagination allows for the ability to efficiently retrieve large datasets from a database by breaking them down into smaller pages. This method is particularly useful when working with large datasets where loading all the data at once would be impractical or slow.

When implementing cursor-based pagination, developers need to keep track of the last record that the user saw. To accomplish this, a "cursor" is sent out to the front-end with each page of results. The cursor then comes back to the database as a token, indicating where the next page of results should start.

**Benefits**

One of the advantages of cursor-based pagination is its resilience to shifting rows. For example, if a record is deleted, the next record that would have followed is still displayed since the query is working off of the cursor rather than a specific offset.

Another benefit of cursor-based pagination is that it can work well with infinite scroll, a design trend that loads content as the user scrolls.

**Drawbacks**

One of the primary downsides of cursor-based pagination is that it's impossible to directly address a specific page. For instance, if the requirement is to jump directly to page five, it's not possible to do so since the pages themselves are not explicitly numbered.

Additionally, cursor-based pagination can be more complicated to implement than offset limit pagination. More thought needs to be put into the structure of the cursor and what criteria should be used to determine it.

#### Deferred Joins

```sql
SELECT
  *
FROM
  people
ORDER BY
  birthday, id
LIMIT 20
OFFSET 450000;


/* deferred join */

SELECT * FROM people
INNER JOIN (
  SELECT id FROM people ORDER BY birthday, id LIMIT 20 OFFSET 450000
) AS people2 USING (id)
ORDER BY
  birthday, id

```

Here, we're using the `USING` clause to specify the matching column between the main table and the subquery. Easier way to specify the joining column.
We're also sorting the results by birthday in ascending order.
If we run this query, we'll see that it takes only 200 milliseconds to execute. That's around three times faster than the traditional pagination!

So how it works is we are reading a lot less data and thus throwing away a lot less since the pagination query is reading a lot less data i.e., by generating a subset of data that contains only the ID column, we're able to apply the pagination on a much smaller dataset. This means we're throwing away less work.

To further optimize the deferred join technique, we can use indexes. If we add an index to the `birthday` column, for example, we can make the inner subquery use a covering index. This means that our pagination can be done entirely on the index without retrieving the actual data.

Here's how we can add an index on the birthday column:

```sql
ALTER TABLE people ADD INDEX birthday (birthday);
```

When we run our optimized query again, we'll see that it takes only 60 milliseconds to execute! That's a full ten times faster than the traditional pagination.

#### Geographic searches 

MySQL has a special data type for a point column, but for this article, we will be using a latitude and longitude column. This method is straightforward and easy to understand but please note that there are more advanced methods for advanced use cases.

Let's start by taking a closer look at these latitude and longitude columns. Suppose we have a table with one million addresses, each of which has a latitude and longitude column. To search for these addresses based on distance, we can use the `stDistanceSphere` function which calculates the distance between two points on a sphere.


```sql
SELECT stDistanceSphere(
  point(lat1, long1),
  point(lat2, long2)
)
```

gives us the distance between two points on the sphere. It is important to note that the calculation is in meters, and we can use this function to make a simple comparison such as whether the distance is less than a specified value.

One of the tricks to calculate the points with a certain range in sphere could be getting all the values in a bounding box and then eliminating the ones outside of sphere since thats expensive.


[Reference](https://planetscale.com/learn/courses/mysql-for-developers/examples/introduction-to-examples)