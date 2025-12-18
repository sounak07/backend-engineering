
HTTPS is not a real time protocol enough for collaboration, so we need a different protocol bidirectional protocol. 
Its difficult to maintain at scale and also to keep them reliable. 

Certain ways to consider. 
- Long polling wouldn't work because it sends a request after every response increasing the latency. State management also becomes difficult. 
- SSE on HTTP/2 needs an extra protocol to become bi-directional
- WebSockets are transport layer level protocol so its hard to find a certain data packets for a specific backend (say there are many services). Also it takes up extra memory 
  
RSockets was the solution. RSocket is a application layer protocol and are based on Reactive stream semantics, basically follows a certain set of rules. 

So what are the advantages of RSockets at scale for the real-time collaboration. RSockets support client-server and server-server communication. 

 **Performance** 
 RSockets support multiplexing. What is means it can support multiple I/O in a single process by dividing the network into separate logical channels and each channel sends the data stream separately.  Also it is possible to mix messages of all the channels. RSocket communication is async. 

**Data Format**
RSocket is layer agnostic, it uses the binary protocol on top of TCP or websockets. 
e.g. - It encodes JSON in binary format and sends it. 

**Flexibility** 
It supports multiple programming languages. Also it offers application level flow control so we dont need to do any extra setup to use it.

**Resilience** 
RSocket support BackPressure independently , basically it supports data flow control to stop the overwhelming of servers causing it to go down.
It also supports implementation of BackPressure in certain channels as per needed. Data analytics will work with some data buffer but data drop might be needed with critical services to have strong consistency. 
Also it supports leasing where client tells the server the number of messages it expects so that it reserves the capacity for it and returns the exact number of messages.

#### Communication Pattern

In RSocket there is no distinction btw client and server once the connection gets established. It supports peer-to-peer communication after this stage, basically bi-directional.

#### Architecture of Canva 

In Canva client Connection is established to websockets Gateway over HTTP, the backend is via RSockets.
With RSockets multiple channels are created with a single connection , so the number of connections are kept low. The least-loaded algo is used to load balance the RSocket connections as the backend connections are mostly long-lived

[Reference](https://newsletter.systemdesign.one/p/rsocket)








