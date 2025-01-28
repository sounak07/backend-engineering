## Consistent Hashing


[Reference](https://www.youtube.com/watch?v=UF9Iqmg94tk)

##### What is hashing ?

Hashing is a technique used to distribute data evenly across multiple servers. It generates a fixed-size string or number using a hash function. The hash function typically generates a number within a known range of values, ensuring predictable distribution.

```
hashed_key = hash(object_id) % n (n = no. of servers)
```

This `hashed_key` is then used to determine which server should data go to for horizontal distribution of data. As long as the hash function is same the key will always map to same server. But the issue arrives when there is a requirement to remove or add new servers. This prompts us to re distribute the keys in each server which can lead to lots of inconsistencies. So consistent hashing comes in place.
##### Consistent hashing

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

There might be inconsistencies in how the servers are placed so the virtual nodes can be used to minimise the load on each server in case they are many keys before that server. In that case one node would have to handle a lot more requests. In order to counter that we can place the same node as virtual nodes in multiple places to ensure uniformity. 

Say instead of hashing "NodeA" once, you could hash "NodeA-1", "NodeA-2", ..., "NodeA-N" to create multiple positions for NodeA on the ring.