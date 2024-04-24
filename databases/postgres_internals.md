## Postgres Internals

##### Connection to Postgres

In Postgres whenever a client connects to it via a TCP connection , a new process gets created. Now these processes are actually managed by a master process called Postmaster , which actually a creates a child process whenever a new connection is established. The child process inherits the TCP connection from the Postmaster though file descriptors. The child process does all the system calls like read, write etc and is also responsible for closing the connection after its done.

Creating a new process might be expensive , too many processes could a create make the database to become unresponsive but this makes the system highly resilient to failures. Even if one of the processes fail, it does not affect other running process.

But to accommodate such a system , Postgres always needs a proxy system in front of it for connection polling. Pg bouncer is one of the most reliable tools for this. It creates a connection pool for the Pg database to be used by the clients so that the db doesn't run out of connections due to limited numbers of processes it can handle. 

[Reference](https://www.youtube.com/watch?v=o7qLKfILuD8)

##### Query Parsing

In Postgres whenever a query is parsed , it first gets converted to tokens. Tokens has a defined set of rules , which tells the parser which token constitute of what rule. Now these rules are mapped to certain actions. 
`CREATE DATABASE` has certain rules to it which when gets matched certain actions are performed. 

So if we see its creating a abstract tree where output of one phase becoming the input of the next one.


[Reference](https://www.youtube.com/watch?v=m8PtOY3aWL0)