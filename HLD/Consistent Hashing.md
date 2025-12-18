[Reference](https://www.youtube.com/watch?v=UF9Iqmg94tk)
[Reference 2](https://www.youtube.com/watch?v=jqUNbqfsnuw)

##### What is hashing ?

A hash function is used generally to create a fixed length value from a arbitrary length value. Its is a technique used to distribute data evenly across multiple servers, dbs. It generates a fixed-size string or number using a hash function. The hash function typically generates a number within a known range of values(modulo hashing), ensuring predictable distribution.

```
hashed_key = hash(object_id) % n (n = no. of servers)
```

This `hashed_key` is then used to determine which server should data go to for horizontal distribution of data. As long as the hash function is same the key will always map to same server. But the issue arrives when there is a requirement to remove or add new servers. This prompts us to re distribute the keys in each server which can lead to lots of inconsistencies. So consistent hashing comes in place.

When a new server is added, we now mod by (N+1) instead of N. This causes cache misses because: Data previously mapped to a specific server is now mapped to a different one. Rebalancing is required to reassign data correctly.

##### Consistent hashing

In a well-designed consistent hashing system, only (1/N) of the total data needs to be reassigned when a server is added or removed.

In consistent hashing both and servers and the keys are hashed to be in a hashed circular space (a ring), a hash function (e.g., SHA-1 or MurmurHash) assigns each node and key a position on this ring and the server that is next to the key in clockwise direction is where the key is put.
This allows shifting of keys to new servers (if added) or to existing servers (if removed) much easier.

1. Let’s assume a system has two servers, `s1` and `s2`, and keys `k1` and `k2`.
   - `k1` hashes to `s1`.
   - `k2` hashes to `s2`.
2. If `s1` is removed from the system, `k1` will now be assigned to `s2` (the next server in the clockwise direction on the ring).
3. Similarly, if a new server `s3` is added, only keys that hash between `s2` and `s3` will be reassigned to `s3`.

Note: The Circular space is a basically a representation of range of values and the highest value wraps back to zero. Whenever a node or data is hashed, a number in that range is generated and becomes its position.

- Node A: `hash("NodeA") → 12345678`
- Node B: `hash("NodeB") → 98765432`
- Node C: `hash("NodeC") → 54321098`

- Key K1: `hash("Key1") → 34567890`
- Key K2: `hash("Key2") → 87654321`
- Key K3: `hash("Key3") → 11223344`

As we can see the nodes and keys can placed in a clockwise direction.

##### Virtual Nodes

While hashing there might be a case where servers are placed inconsistently so the keys might need to be handled by one server as below -

![Screenshot_2025-05-18_at_3.43.51_AM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2025-05-18_at_3.43.51_AM.png)

Virtual nodes can be used to minimise the load on each server in case they are many keys before that server. Virtual nodes are basically replicas of servers placed randomly at different places in the circular hashed servers.
Basically what we can do is if we have 3 servers placed after hashing, we create a few more random hashed of these 3 servers and place them in the circle.
The decision of the number of virtual nodes depends on the factor that we want to perform (1/n % total keys) rebalances in case of server add/delete.

In that case one node would have to handle a lot more requests. In order to counter that we can place the same node as virtual nodes in multiple places to ensure uniformity.

![Screenshot_2025-05-18_at_3.46.19_AM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2025-05-18_at_3.46.19_AM.png)

Say instead of hashing "NodeA" once, you could hash "NodeA-1", "NodeA-2", ..., "NodeA-N" to create multiple positions for NodeA on the ring.
