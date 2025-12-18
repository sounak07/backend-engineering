Monoliths have their own problems, so Microservices came into play but they also have their drawbacks unless properly planned. Patterns can be a way through this. Lets see how.

[Microservices.io Patterns](https://microservices.io/patternsl)

Each phase of creating microservice can be divided into parts and each part can designed following certain patterns.
There are patterns for

- decomposition, how the services needs to be broken down
- database, how the database should look like, should each microservice have one database.
- Communication
- Integration
  and many more.

![Screenshot_2025-05-08_at_12.38.51_AM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2025-05-08_at_12.38.51_AM.png)

##### Decomposition Pattern

- Decomposition by business capability
  - Divide by business capability. Knowing what your business functions are is important to apply like pattern. There is no definition of micro, like many services there should be , it depends on the requirements.

    Say we need inventory management, there we need a services for billing, payment, user management, store management, order management etc.
- Decomposition by Sub domain
  - Divide by sub domain , basically dividing the services by the type of task. Say the domain is order so there could order received, order returns, order inventory etc. For payments it could payment received , one for payment received.

##### Strangler Pattern

- **\*Purpose**:\*
  Gradually refactoring a monolithic application into microservices.
  **_How it Works:_**
- A "controller" is introduced to handle requests.
- Initially, the controller forwards all traffic to the monolithic application.
- Gradually, specific functionalities are extracted into microservices, and the controller routes traffic to them.
- As more functionalities are migrated, the controller forwards less traffic to the monolithic application, eventually strangling it.
- _Advantages:_ - Minimizes disruption to existing services. - Allows for a gradual transition to microservices.
  **\*Example**:\*
- Imagine a monolithic e-commerce website being refactored into microservices.
- The controller initially directs all traffic to the monolithic website. - Gradually, functionalities like order placement, inventory management, and payment processing are moved to individual microservices.
- The controller gradually routes more traffic to these microservices, eventually reducing the reliance on the monolithic application.

##### Data Management in MS

- Shared database - Common db shared among microservices.
- Individual Database - Each service has its own database.

_Why Database per Service is Preferred:_

- _Scalability:_ Allows for independent scaling of individual services without impacting others.
- _Isolation:_ Changes in one service's database don't affect others.
- _Technology Flexibility:_ Services can choose different databases based on their specific needs.

Shared database also have their advantages of joining queries easily , maintaining ACID properties etc, but it comes at a cost of difficulty in scaling for specific requirement needing to scale for all which might not be needed. Also performance bottlenecks would be there when multiple services start accessing same database.

##### SAGA Pattern

When there are multiple databases for each service and there is a need to maintain ACID across all of them due to some request that updates db in all the services in a transactional way SAGA comes into play. Managing distributed transactions across multiple databases is what SAGA plays an important role.

SAGA is known as Sequence of local transactions.Purpose is Managing distributed transactions across multiple databases, ensuring data consistency even if some operations fail.

In SAGA pattern what happens is,

- A sequence of local transactions is executed within each participating microservice.
- Each transaction updates the database and publishes an event.
- Subsequent transactions listen to these events and continue the process.
- In case of failure, compensation events are published to undo completed operations and maintain consistency.

_Types of Sagas:_

- **Choreography** - Here each service publishes an event, say in a queue for each local transaction success and the subsequent service reads it and proceeds, exactly as described above.
  The problem here is there could be a cycle dependency among services here.
- **Orchestator** - Here an orchestrator actually controls how the services behave based on local transactions. What happens is whenever a service completes its transaction it sends an event to the orchestrator and it directs the subsequent service to proceed. If anything fails the service informs that to orchestrator and it acts according instructing the previous services to rollback.

Interview Questions can asked on how to handle payments from one account to another if while sending payment fails.
It can addressed using SAGA, whenever payment fails the receiver generates and event and the sender listening to it rollbacks the money deduction transaction.

##### CQRS Pattern (Command Query Request Segregation)

This pattern is useful for a case where we need to join multiple tables/ run query on tables from different databases of different services.

Basically its segregates read(query) and command(write - CUD) operations by creating a db view(combined) for all the tables across services.

- _Example:_ - A blog application where write operations are performed on a relational database, while read operations access a denormalized view optimized

This new common db needs to be updated for consistency. So there are few ways to achieve this -

- Create Events whenever new changes are made on any of the dbs and update the view db.
- Db triggers/procedures can also be used to update the view db.
