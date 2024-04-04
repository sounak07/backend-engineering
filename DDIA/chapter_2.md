## Chapter 2 - Data Models and Query Languages

Data models represent how we want to store data of an application. Applications are built layering data models on top of each other eventually providing a cleaner data model. These data models allow different abstraction to work together since they provide an interface on how to communicate with each other.

#### Birth of NOSQL

How and why did this buzzword flourish all of a sudden. 
- A need for greater scalability for larger data sets with very high throughput.
- Restrictions around Relational models and need for more dynamic and flexible data models.
- No support for Specialised queries for certain cases.
- A widespread preference of free and open source tools.

#### Object Model Mismatch

Most of the application code these days are written following OOP models. So there is a mismatch in tables and objects with which we deal with in code. ORM can solve in bridging this gap to some extent but still there will certain aspects and tradeoff to it.

#### Document vs Relational Model

Its hard to pick one type of database and is highly dependent on the type of application you are trying to build.

***Document models*** goes ahead in flexibility , data locality and performance , ahead in storing data structures that are used by the application code.
***Relational models*** are ahead in providing the ability of joins and many-to-many relationships. Better indexing of cols etc.

If the requirement to access the entire tree at once is there without needing to a get a specified nested object frequently , document model could be a good choice.
Data that are very related to each other with complex relationships(many-to-many) within them, relational is a better choice.
Its possible to minimise joins by denormalising but the complexity in application code increases in that case.
*Note: Refer to page 33 for normalisation explanation.*
Joins can also be emulated in application code by making multiple requests in document model but that increases the overall complexity and is usually slower than actual joins in Relational databases.

#### Schema Flexibility in Document dbs

As we know there is a lot of flexibility around schemas in document dbs. Document databases don't enforce any schemas for the data stored in them, so they are often called *schema less*, but thats a bit incorrect. 
The code that reads the data always expects certain kind of structure in it, so its actually a *schema-on read*, so this is an implicit schema but not enforced by database , in contrast to *schema-on write* in case of relational dbs where the database enforces the data type that can be written into the database.
So *schema-on read* is similar to dynamic type checking in certain language and *schema-on write* is compile time type checking in some. 

An example of how schema flexibility can effect data storage and extension can be found in Book's *page 40*. 

#### Data locality in Queries

Document databases store data in a single continuous string as encoded JSON, XML or Binary encoded JSON (BSON in case of Mongodb). If there is a requirement to load the entire document document model could be performant because join a bunch of tables to achieve all data could be not. 

The data locality is useful if you need large parts of document at once but in case of updates large files might not be performant as we need to read and then write entire file after update and if the file size is too large it might not be performant. 

Data locality is not limited to Document databases but are also available to some relational dbs as well such google's Spanner database by allowing the schema to declare that the data should be stored in a nested way within parents table. 

#### Query languages in Data

SQL is a declarative language , meaning we declare the pattern of data we want and let the language decide how it wants to retrieve the data how it wants to use indexed, if it wants to use joins , how it wants to return the data. 
Declarative languages are easy to use since it hides the actual implementation. 
The returned data might not be of same order every time since it doesn't guarantees order.

```sql
Select * from animals where animal = 'dogs'
```

Most of the languages however are imperative where we specify reach set of instructions which needs to be performed in order. 
One of the advantages of declarative language is its ability to execute operations parallaly which is difficult to do in imperative languages since it needs to a follow a certain order to complete the operations.

#### Declarative Queries on the web

CSS actually uses declarative language in the web browser. It would be very difficult otherwise to do style manipulations using javascript which is a imperative language. 

*Refer to Book's page 44 for example*

#### MapReduce Querying 

MapReduce is programming model for handling large quantity data. Its neither declarative nor imperative. Its somewhere in the middle.

*Refer Book's page 46 for example comparison*  

#### Graph Like data Models

When the relationships are mostly one-to-many or no relations, document databases could be a right fit. But with many-to-many relationships in place SQL is probably the best bet.
But relationships with more complex relations could be stored via graph based dbs like facebook uses graph dbs to store comments , events, posts, locations etc which are basically vertices  and the edges represent the people , whom they are friends with , who commented on which post etc.

See book page no. 52 for examples

#### Triple stores

In triple stores data is stored as three statements, subject, predicate and object. Its quite similar to graphs. Subject will always be a vertex. The object can be represented in 2 ways.

- As a value in a primitive data type. In that case predicate and object are represented as key-value pair like (Lucy, age, 33) is represented as Lucy as vertex and  {"age": 33} as property of that vertex. 
- As a vertex in the graph. In that case predicate becomes an edge and subject and object becomes 2 edges of the edge.

There were plans to use Triple stores to represent websites in semantic web using RDF data model. Refer to book page 57 for more info. 

#### The Cypher and SparkQL Query languages

The cypher and SparkQL are languages for querying Graph data models and RDF data models respectively. The cypher is actually drawn from SparkQL which is why there are quite similar. 
If we see below the structure is quite similar to each other 

Cypher Query

![[Screenshot 2024-03-12 at 10.52.44 AM.png]]

SqarkQL Query 

The SqarkQL is used to query triple store using RDF.

![[Screenshot 2024-03-12 at 10.53.39 AM.png]]

### The Foundation : Datalog

Datalog represents data similar to Triple Stores but here its stored as `predicate(object, subject)` . We can say the data is represented in the form of facts and rules. 
Say `employee(john, developer)` indicating that "John" is a "developer" is a fact. 
Rules creates a logical relationship between the facts. 

A rule might state that `manager(X) :- employee(X, manager)` indicating that if someone is an "employee" and has a role of "manager", then that person is also categorised as a "manager".

 Datalog kind of creates a chain of predicates that is generated from other rules. It requires a bit of different thinking to use datalog since rules needs to be combined and reused but can be powerful for complex datasets. 



[Mind Map](https://trunin.com/en/2021/12/designing-data-intensive-apps-part02/images/_hu746bba5dfb826d8cbcee0ea76b1b56f6_857685_93d2cd8d4ea25f5444447d4d7cdc6185.webp) 
