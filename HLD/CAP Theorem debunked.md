CAP theorem statements that out of the three properties _Consistency_ , _Availability_ and _Partition tolerance_ , a distributed system can only provide two of them at the same time. It formalises the trade off between consistency and availability in some sense.

**Consistency** - All nodes display the same data , guaranteed the writes are reflected at all nodes for the most recent writes.

**Availability** - All requests return a response without guarantee that the data is the most updated one. All nodes should respond. If all db nodes are responding its available.

**Partial Tolerance** - The system continues to function even if there is network failures between nodes. So user can query the nodes and get data, might not be consistent or some nodes might not be available but system is working.

Lets say we have a system as below where due to network outage communication between two nodes have been disrupted.

![draw2](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/draw2.png)

Here we have two options -

- We fail the request compromising _availability_
- We allow the request to go through returning a stale value from the Node 2, since it not been updated compromising consistency.

Based on the systems requirements we have to decide the tradeoffs since we can't ensure both of them.

Suppose there is a system where we can all , CAP (which is not possible), lets see what happens.

**AP** - Say one of the nodes(partitions) goes down, now there is no communication between nodes, its not consistent any more. Our system is available(A) and running(P) but lacks consistency so its a AP system. CAP is not possible here.

**CP** - Similarly if we cant consistency at any cost, but there is no communication between nodes, we need to take down the node thats has outdated data. So this system is Consistent(C) and running and responding(P) but not all nodes are available.

**CA** - Similarly we can consistency and availability, it that case if there is no communication between nodes, we need to take down the whole system (no P) until fixed, so its Consistent(C) and available(A) but not Partition tolerance since

Having Partition tolerance is very important since most systems are distributed.

Lets take example of NOSQL DBs to understand how we can implement CAP

**_CA databases_**
These databases will ensure consistency and availability but no partial tolerance. In distributed systems, partition is bound to happen so this approach might not be very practical.

**_CP databases_**
These databases will ensure consistency and partial tolerance but not availability. MongoDB is a great example for this which maintains a primary node and all its secondary nodes syncs itself to the primary one ensuring the data consistency.
Whenever there is a inconsistent node, the system has to turn off until the node is fixed.

**_AP databases_**
These databases will ensure partial tolerance and availability but not consistency. Apache Cassandra is a great example for this which has no primary nodes which means all nodes remain available. In case request comes to an inconsistent node , user will receive an old version of the data making the overall system inconsistent. On resolving the fault all the nodes will re-sync with each other making all the nodes updated to the latest version.

[Reference](https://www.educative.io/blog/what-is-cap-theorem#whatiscaptheorem)
