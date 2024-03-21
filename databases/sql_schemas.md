Database schemas should be 
- Small - Choose the smallest data type that can hold your data. 
- Simple - Choose the correct data type for the data that we are trying to store. Use `int` for integers , `datetime` for dates. *Don't use string for dates*
- Honest - Being honest with the data you are going to store. Don't extend it to store billions if its only going to go upto 100.

Here we are not really optimising for space but for compactness , which will allow the database to access the data much faster. Also it will make indexing the dataset much easier and faster to achieve. 

##### Integers

![alt text](/resources/Screenshot%202024-02-18%20at%2011.46.49 PM.png)

A `TINYINT` can store 1 byte or 8 bits so it can store 0 to 255 as shown or -128 to 127 in case it supports `-ve` numbers.

![alt text](/resources/Screenshot%202024-02-18%20at%2011.51.28 PM.png)

`-ve` or `+ve` is represented by an extra bit as shown.
Its -128 for negative because 0 is not considered in the negative side but its from -1 to -128. This is to avoid ambiguity around representing 0 as -0 or +0.

![alt text](/resources/Screenshot%202024-02-18%20at%2011.54.09 PM.png)
We choose `SMALLINT` since its seems like a more realistic number for the number of pages. We tell the db that we are not interested in storing `-ve` by `UNSIGNED` keyword.

*Note :There are case of trying to change `INT` like as `INT(3)` , but this wrong.*

##### Decimals

Data types available to store in decimals are 
- Decimal (exact representation) 
- Double, Float (Approximation) 

So we want to store exact value we want to use decimal otherwise we use float or double.

```sql
create table dec (
	int n,
	d1 decimal(10,2)
)
```

(10, 2) represents that there are 10 digits we can store of which 2 goes after decimal.

##### Strings

Data types available to store in decimals are 

![alt text](/resources/Screenshot%202024-02-27%20at%2011.27.20%20PM.png)

`char` is going to occupy full space allowed while `varchar` only occupies whats needed. 
![alt text](/resources/Screenshot%202024-02-27%20at%2011.38.32%20PM.png)

CHARSET determines the type of chars allowed in the table. `information_schema` table has all the supported ones along with COLLATE.
`utf8mb4` supports all kinds of chars including emojis so thats why its default.

COLLATE is how we can compare the chars in table.
`utf8mb4_0900_ai_ci` means its case insensitive (a == A) and its accent insensitive. (e == é)

##### Long strings 

`TEXT` can be used to store very long texts that goes beyond 1000 chars. `TEXT` can be of different types like 
`TINYTEXT`  (256 chars), barely used over `VARCHAR`
`TEXT` (65000 chars),
`MEDIUMTEXT` (16 MBs), 
`LONGTEXT` (4 GBs)

`BLOB` can be used to store huge binary data. Can be used to store files actually. 

##### ENUMS

They are the allowed sets of string into the database table.
![alt text](/resources/Screenshot%202024-02-28%20at%2012.18.49%20AM.png)
![alt text](/resources/Screenshot%202024-02-28%20at%2012.16.56%20AM.png)

But `ENUMS` are actually stored as a number in db as we can see above. So we get the readability of a string and compactness of an integers. 
The numbers are based on the declared order so small is 2. 
So when we sort the cols, it will actually sort it based on the order of ENUMs and not chars in string. 
*Note: 0 is reserved for the invalid data.*

##### Dates

![alt text](/resources/Screenshot%202024-03-03%20at%207.26.41%20PM.png)

- DATE if you only need to store dates. 
- TIMESTAMP can only store till 2038, so the 2038 problem. DATETIME however can store till 9999-12-31.
- TIMESTAMP helps with timezones , so what it means is whenever data is stored as TIMESTAMP it stores the data in UTC but while retrieving it actually converts it to the user's timezone. 

![alt text](/resources/Screenshot%202024-03-03%20at%207.35.43%20PM.png)

As we can see we can update `updated_at` with current stamp but on update.
##### JSON

![alt text](/resources/Screenshot%202024-03-03%20at%207.42.48%20PM.png)

While trying to insert `JSON`, MYSQL actually validated it. JSONs can also be stored in `TEXT` but we should not because it won't validate the incoming JSON.
`->`  can be used to access a key a like `->"$.key"` , it will return value with quotes, but with` ->>` value can be accessed without quotes. 

We can't index the entire JSON but a certain key inside the JSON.

##### Unexpected Types

![alt text](/resources/Screenshot%202024-03-10%20at%203.48.22%20PM.png)

As we can see there is no boolean type in the database , its just a tiny int. 

A case where we need to store the IP address we have two options, we can store as a string or we can use a function called INET_ATON to convert that to an integer and INET_NTOA to reverse the convert.

This could be significant since spotting the wrong IPs , comparing ranges , finding the missing part gets easier this way. 


##### Generator columns 

Generator columns refer to the data which can be generated on the fly and populated into the database. There can be quite a few use cases with this. One of them could be 
![alt text](/resources/Screenshot%202024-03-10%20at%204.04.24%20PM.png)

Other cases could be trying to generate some hash of multiple functions or do some math and insert some data.
One thing to keep in mind is that the values has to be deterministic and not something changes everything like rand(), now() etc.

There are two types of generator columns - STORED and VIRTUAL 

 A stored generated column is computed when it is written (inserted or updated) and occupies storage as if it were a normal column. A virtual generated column occupies no storage and is computed when it is read.

![alt text](/resources/Screenshot%202024-03-10%20at%204.29.54%20PM.png)




[Reference](https://planetscale.com/learn/courses/mysql-for-developers/schema)