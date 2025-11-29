## Kafka for dummies

#### Message in Kafka

The kafka message has 3 parts -

- Headers (Topics and Partitions)
- Key
- Value

![alt text](/resources/Screenshot%202025-11-18%20at%201.17.41%20PM.png)

![alt text](/resources/Screenshot%202025-11-18%20at%201.28.04%20PM.png)

A real world example for partitions could be having partitions for different types of payments say for Topic A, P1 - Credit cards , P2 - UPI, P3 - COD etc.

![alt text](/resources/Screenshot%202025-11-18%20at%201.28.26%20PM.png)

**Key determines the partition the message should go in and inserted in order**.

Without key kafka distributes the messages among the available partitions to balance load, order is not maintained across all the partitions of the topic.

Putting everything in one partition could hammer that leading to failures, choosing the right key is important.

Say partition key is chosen as movie id , if that movie is streamed by a lot of people , same partition will be hit leading to choking things. Instead pick a compound keys.

![alt text](/resources/Screenshot%202025-11-18%20at%201.34.29%20PM.png)

**Brokers**

A Kafka cluster is made up of multiple **brokers**. These are just individual servers (they can be physical or virtual). Each broker is responsible for storing data and serving clients. The more brokers you have, the more data you can store and the more clients you can serve.

**Partitions**

Each broker has a number of **partitions**. Each partition is an ordered, immutable sequence of messages that is continually appended to -- think of like a log file. Partitions are the way Kafka scales as they allow for messages to be consumed in parallel.

**Topics**

A **topic** is just a logical grouping of partitions. Topics are the way you publish and subscribe to data in Kafka. When you publish a message, you publish it to a topic, and when you consume a message, you consume it from a topic. Topics are always multi-producer; that is, a topic can have zero, one, or many producers that write data to it.

#### Managing Consumer

When there is too much load for one consumer to handle, we can add multiple consumers consuming from same partition, this group of consumers is called Consumer groups.

![alt text](/resources/Screenshot%202025-11-18%20at%203.18.24%20PM.png)

Consumer groups allow multiple consumers to work together; kafka makes sure each consumer(from each group) only processes one message only once.
Say  
Partition P1 can only be consumed by Consumer C1 and C2.
P2 can only be consumed by C3.
During failure say C1 fails, kafka corrects ifself to let C2 consume all the messages from P1.

![alt text](/resources/Screenshot%202025-11-18%20at%201.43.19%20PM.png)

#### Data persistence

Consumers track the last processed message using offsets telling the consumer which message was processed last and which to process next. This data is saved in kafka.
Saving the correct data is crucial since in of a crash consumers will pick up from the offset , committing to early would loose the messages and late commits could to lead to processing same message twice.

![alt text](/resources/Screenshot%202025-11-18%20at%201.38.53%20PM.png)

#### Delivery Guarantees

Three delivery Guarantees are offered.

- AtMost once, might loose messages
- Atleast once, no loose but duplication can happen
- Exactly once, no loose, no duplication, hard to setup

#### Replication and Durability

Replication in kafka comes with leader and followers. Each leader handles read and writes propagating its data(copy) to its followers , if a leader fails the follower takes over as the new leader without any failures.

![alt text](/resources/Screenshot%202025-11-18%20at%201.50.37%20PM.png)

Kafka can be configured to wait for writes in all followers but that is very slow but very safe.

#### Real World examples

Uber drivers propagating live locations of cars. Uber uses Partitions as per geography to allow maximum scalability.

![alt text](/resources/Screenshot%202025-11-18%20at%201.52.39%20PM.png)

![alt text](/resources/Screenshot%202025-11-18%20at%201.52.57%20PM.png)

#### Trade-off and Limitations

- It optimises for Throughput not latency
- Not suitable for Request-Response patterns
- Kafka guarantees order only within a single partition not across an entire topic, so parallelising could be difficult. Partial ordering is accepted in most cases.

#### How Kafka works

When a message is published into a topic in kafka , kafka determines the partition which this message needs to go. They are few steps -

**Partition determination** - The partition can be specified as a key in the message, if no key is specified , a round-robin randomly assigns a partition(No Ordering guarantees).
But when a key is specified , kafka uses its hash algo to hash the key and assign to correct partition.

**Broker Determination** - Once partition is determined , broker where the partition is stored is determined usually by the controller using the kafka meta data which holds the mapping btw brokers and partitions.

Partitions of kafka are append-only log files which are stored in disk. Messages gets appended at the end of the file with an offset set to it. Benefits of doing this include -

- Immutability - Files cannot be edited once committed
- Efficiency - Hurdle of seeking disk is minimised (append-only)
- Scalability - Scaling to multiple log files is easier

Each consumer uses the offset of data in partitions to determine what it is they read last and go from there. Consumers commit the last offset read data periodically to kafka to avoid getting lost in event of a crash.

Consumers read messages from Kafka topics using a **pull-based model**. Unlike some messaging systems that push data to consumers, Kafka consumers actively poll the broker for new messages at intervals they control, this pull approach was a deliberate design choice that provides several advantages: it lets consumers control their consumption rate, simplifies failure handling, prevents overwhelming slow consumers, and enables efficient batching.

![alt text](/resources/Screenshot%202025-11-18%20at%209.45.46%20PM.png)

#### When to use Kafka

### As a Message Queue

**Youtube**

![alt text](/resources/Screenshot%202025-11-18%20at%209.50.29%20PM.png)

You have processing that can be done asynchronously. YouTube is a good example of this. When users upload a video we can make the standard definition video available immediately and then put the video (via link) a Kafka topic to be transcoded when the system has time.

**InOrder Message Processing (Ticket bookings)**

![alt text](/resources/Screenshot%202025-11-18%20at%209.51.00%20PM.png)

**Decouple producer and Consumer**

![alt text](/resources/Screenshot%202025-11-18%20at%209.53.20%20PM.png)

You want to decouple the producer and consumer so that they can scale independently. Usually this means that the producer is producing messages faster than the consumer can consume them. This is a common pattern in microservices where you want to ensure that one service can't take down another.

### As a stream

**Ad Click Aggregator**

![alt text](/resources/Screenshot%202025-11-18%20at%209.55.02%20PM.png)

You require continuous and immediate processing of incoming data, treating it as a real-time flow. See [Design an Ad Click Aggregator](https://www.hellointerview.com/learn/system-design/problem-breakdowns/ad-click-aggregator) for an example where we aggregate click data in real-time.

**Live Comments**

![alt text](/resources/Screenshot%202025-11-18%20at%209.55.51%20PM.png)

Messages need to be processed by multiple consumers simultaneously. In [Design FB Live Comments](https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-live-comments) we can use Kafka as a pub/sub system to send comments to multiple consumers(all the other users watching the live video/comment).

#### What to know about Kafka

### Scalability

**Constraints**
Aim for < 1MB per message

![alt text](/resources/Screenshot%202025-11-18%20at%2010.01.41%20PM.png)

One broker could store upto 1TB data(append-only logs files) and process 10k msg/sec

How to scale?

- More brokers
- Choose a great partition key strategy

Not having a good partition key strategy could lead to hot partition. Even with good key due to some reasons one partition is getting hammered with lots of events, how do we handle that ??

- Remove the key, LOL. But if you dont need ordering, this is the simplest approach.
- Compound keys with Hash
  ![alt text](/resources/Screenshot%202025-11-18%20at%201.34.29%20PM.png)
- Backpressure - Slow down the Producer

### Fault Tolerance and Durability

Having a leader-follower architecture helps here a lot. One of the important things is how that architecture plays.Correct Kafka configs are essential here.

```
acks (acks=all) //Wait till leader copies to [acks=all] its followers
replication factor (3 is fault) // number of followers
```

How we choose to use this is based on trade-off for durability we need to make based on system. Usually kafka doesn't due its durable architecture

**Consumer is Down**

Consumer commits the offset regularly ,so if it goes down it will come back up and pick up from there, committing to early would loose the messages and late commits could to lead to processing same message twice.

### Retries

**Producer**

```js
const producer = kafka.producer({
  retry: {
    retries: 5, // Retry up to 5 times
    initialRetryTime: 100, // Wait 100ms between retries
  },
  idempotent: true,
});
```

**Consumer Retries**

Kafka does not actually support retries for consumers out of the box (but [AWS SQS](https://aws.amazon.com/sqs/) does!) so we need to implement our own retry logic. One common pattern is to set up a custom topic that we can move failed messages to and then have a separate consumer that processes these messages. This way, we can retry messages as many times as we want without affecting the main consumer. If a given message is retried too many times, we can move it to a dead letter queue (DLQ). DLQs are just a place to store failed messages so that we can investigate them later.

![alt text](/resources/Screenshot%202025-11-18%20at%2010.24.21%20PM.png)

### Perfomance Optimisations

**Batch Messages in producer**

```js
const producer = kafka.producer({
  batch: {
    maxSize: 16384, // Maximum batch size in bytes
    maxTime: 100, // Maximum time to wait before sending a batch
  },
});
```

**Compress Messages on Producer**

Kafka supports several compression algorithms, including GZIP, Snappy, and LZ4. Essentially, we're just making the messages smaller so that they can be sent faster.

```js
const producer = kafka.producer({
  compression: CompressionTypes.GZIP,
});
```

Arguably the biggest impact you can have to performance comes back to your choice of partition key. The goal is to maximize parallelism by ensuring that messages are evenly distributed across partitions. In your interview, discussing the partition strategy, as we go into above, should just about always be where you start.

### Retention Policies

Kafka topics have a retention policy that determines how long messages are retained in the log. This is configured via the `retention.ms` and `retention.bytes` settings. The default retention policy is to keep messages for 7 days.

In your interview, you may be asked to design a system that needs to store messages for a longer period of time. In this case, you can configure the retention policy to keep messages for a longer duration. Just be mindful of the impact on storage costs and performance.

#### Kafka vs Rabbitmq

![alt text](/resources/Screenshot%202025-11-19%20at%2011.45.50%20AM.png)

1. kafka is much more expensive to run, especially because of the persistence
2. rabbitmq is generally slower at processing messages (hence unsuitable for streaming)
3. kafka has a lot more plugins for different backend services
4. rabbitmq is relatively simpler conceptually hence faster to integrate

![alt text](/resources/Screenshot%202025-11-19%20at%2011.47.49%20AM.png)

![alt text](/resources/Screenshot%202025-11-19%20at%2011.48.16%20AM.png)

### 🔥 **Conceptual Difference (Deep but Simple)**

🐇 **RabbitMQ**

- Messages go **into a queue**.
- A consumer reads a message, **the message disappears**.
- It’s built for **task distribution**, **short-lived messages**, and **work queues**.

🦄 **Kafka**

- Messages go into a **partitioned log**.
- Messages **do NOT disappear**.
- Consumers track **their own offsets**, meaning:
  - They can rewind
  - Replay messages
  - Have multiple independent consumer groups reading the same topic

Kafka is built for **event streaming**, **data pipelines**, **high throughput**, and **replayable immutable logs**.

---

### 🧠 **Mental Model (Most Important)**

Think of it like this:

RabbitMQ = WhatsApp

You send a message → the recipient consumes it → it disappears.

Kafka = YouTube

You upload a video → millions of people (consumer groups) can watch it, rewatch it, or watch from different points.  
The video _never disappears_ unless retention deletes it.

### 🎯 **Use Case Differences (The Real World View)**

🐇 **RabbitMQ Best For**

- Background jobs (Celery)
- Task queues
- RPC between microservices
- Request/response patterns
- Low-latency commands
- Small-scale systems

If the message represents **work to be done**, RabbitMQ wins.

---

🦄 **Kafka Best For**

- Event-driven microservices
- Audit logs & immutable events
- Real-time data processing (streams)
- CDC pipelines (Debezium)
- Analytics ingestion (clickstreams)
- Log aggregation
- Replayable messages
- High throughput distributed systems
- ML feature pipelines

### Diagrams

**RabbitMq**

```sql

             [ Producer ]
                  |
                  v
            +--------------+
            |   Exchange   |
            +--------------+
                  |
                  v
           +---------------+
           |    Queue      |
           +---------------+
         /        |         \
        v         v          v
 [Consumer1] [Consumer2] [Consumer3]

- Broker PUSHES messages to consumers
- Message is removed after consumer ACK
- Message can only be read by any one of the consumer

```

**Kafka**

```sql
                      [ Producer ]
                           |
                           v
  +---------------------------------------------------------+
  |                Kafka Topic (Log)                        |
  |  Partition 0: [e1][e2][e3][e4][e5] ....                  |
  |  Partition 1: [e1][e2][e3][e4][e5] ....                  |
  |  Partition 2: [e1][e2][e3][e4][e5] ....                  |
  +---------------------------------------------------------+

         ^            ^             ^
         |            |             |
   Offset=5      Offset=2     Offset=10
    Consumer A    Consumer B    Consumer C

- Consumers PULL messages
- Messages remain in log
- Each consumer keeps its own offset

```

#### References

[ByteByteGo](https://www.youtube.com/watch?v=7_wkWQ9rB5I)
[Nana](https://www.youtube.com/watch?v=B7CwU_tNYIE&t=40s)
[Kafka Setup](https://gitlab.com/twn-youtube/kafka-crash-course/-/tree/main?ref_type=heads)
[Hello Interview](https://www.hellointerview.com/learn/system-design/deep-dives/kafka)
