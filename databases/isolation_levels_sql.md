## Isolation Levels in SQL

#### ACID

SQL databases guarantees ACID based transactions. The ACID stands for -
- **Atomicity** - It guarantees that the transactions are atomic, either its completely done or not. It case of failures , the entire transaction is rolled back.
- **Consistency** - It guarantees that the transactions are allowed to change the state of the database from one to another, leaving it in a state as per certain rules and constraints. 
- **Isolation** - It guarantees that the transactions are isolated from each other to avoid race conditions , dirty reads , bad reads etc. The level of Isolation decides how it maintains data consistency and concurrency. 
- **Durability** - It guarantees the durability of the data once its committed even if the database cluster crashes. This is usually done by logging , redundancy, recovery mechanisms etc.  

#### Isolation levels

There are various levels of Isolation -

**Read Uncommitted** - This type of Isolation level allows you to read uncommitted data by other transactions which might introduce to dirty reads. In this case level of concurrency is the highest but data consistency on reads gets affected. 

**Read Committed** - This type of Isolation level allows you to read only committed data by other transactions. This ensure no dirty reads but fails to prevent non-repeatable reads, where reading the same row in the transaction can result in different values being read.

**Repeatable Reads** - This type of Isolation level prevents non-repeatable reads, i.e. repeated queries reads would always return the same value. However it fails to prevent phantom reads because of other transactions changing other columns in the database. 

*One example would be user1 added an item to the cart but even before committing the payment, user2 came in and bought it resulting user1 to get an error of item is out of stock.*

**Serializable** - This offers the strictest form of Isolation ensuring no dirty reads, non-repeatable reads and phantom reads. This affects the concurrency heavily since it feels like running things sequentially. 


[Reference](https://pratikpandey.substack.com/p/database-basics-series-understanding)




