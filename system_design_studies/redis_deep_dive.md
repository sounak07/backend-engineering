## Redis Deep Dive

- Redis is single threaded. So its easier to use and implement without having to worry about concurrency.
- Redis is In-memory
- Redis can store any type of Data structure; str, list, bloom filters.

##### Commands

Redis CLI supports a bunch of commands

```
SET foo 1
GET foo     # Returns 1
INCR foo    # Returns 2
XADD mystream * name Sara surname OConnor # Adds an item to a stream
```

##### Infrastructure

Redis can run as a single node with a replica or as a cluster.
Even they clusters can have their replicas reading from main.
