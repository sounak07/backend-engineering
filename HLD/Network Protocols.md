Network protocols define the rules on how two services can communicate. They can only communicate if they understand similar languages and have similar set of rules in place.
The network protocol has 6 layers mostly.

- Application -> Presentation -> Session -> Transport -> Network -> Datalink -> Physical

Most important of them are Network Layer and Transport layer.

[Excali Draw](https://app.excalidraw.com/l/56zGeHiLyKZ/nfrypwDYa4)
[Source](https://www.hellointerview.com/learn/system-design/core-concepts/networking-essentials)

![Screenshot_2025-06-04_at_11.36.17_AM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2025-06-04_at_11.36.17_AM.png)

#### Application Layer

Application layer serves mostly 2 types of Protocol

- Client-Server Protocol

  - HTTP
  - SMTP
  - FTP
  - Web sockets

  Client server models in a one way comm, client initials a request and server responds, same for HTTP , SMTP, FTP

  Web sockets however is a bidirectional comm protocol but is not a peer to peer because here clients and server talk to each other in bidirectional manner but 2 clients do not interact. So this is not a Peer-to-peer protocol. Web sockets should be designed in a typical request-response format , we can but thats not whats web sockets are for. Web sockets involves state.

  **HTTP (Hyper text transfer Protocol)** - Connection oriented , 1 connection is created and web pages are accessed via hyper texts to jump from one page to another.

  **FTP (File Transfer Protocol)** - Connection oriented, 2 connections are created. Control connection is maintained but data connection can be disconnected. Transferring files between computers.

  **SMTP (Simple Mail Transfer Protocol)** - Sending a mail.
  **IMAP (Internal message access Protocol)** - Works with SMTP for Accessing and reading of mail.
  POP - Its redundant , it downloads and reads the email.

  In case of SMTP , there is server and client where User agent -> MTA Server(Message transfer agent) -> MTA Client -> End user. So client server is in place.

- Peer-to-peer Protocol
  - WebRTC allows clients to talk to each other directly without needing to go to server thats why its very fast.
    ![Screenshot_2025-06-04_at_12.36.16_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2025-06-04_at_12.36.16_PM.png)

#### Transport Layer

- TCP/IP
  - In TCP data is transferred after establishing connections
  - Connection-oriented (establishes a virtual connection). - Divides data into packets and ordering is maintained. After transfer acknowledgement happens.
  - Error in transmission prompts resend.
  - Slow but reliable.
  - eg. - WhatsApp, applications requiring reliable data transfer.
- UDP/IP
  - No connection is established, data is sent without connections and no order is maintained.
  - Very fast , data loss can happen.
  - eg. - Live streaming
- TCP provides reliable data transfer, while UDP prioritises speed
- In TCP , connection is established with 3 way handshake. Client sends, server acknowledges and sends back acknowledgement , client acknowledges server.
- **UDP (User Datagram Protocol)**: No connection is established—just sends data directly (no handshake) to the receiver's IP and port.

#### Important points

- **HTTP**: Built on TCP, so it uses the TCP handshake under the hood. HTTPS provides secure transfer.
- FTP is generally not used since its data connection is not secured.
- We use HTTPS for secure and encrypted data connections.

#### Comparison: HTTP vs WebSocket vs WebRTC

| Feature             | HTTP          | WebSocket     | WebRTC         |
| ------------------- | ------------- | ------------- | -------------- |
| Communication Model | Client-Server | Client-Server | Peer-to-Peer   |
| Connection Type     | Stateless     | Persistent    | Persistent     |
| Protocol Type       | TCP           | TCP           | UDP            |
| Used For            | Browsing      | Chat Apps     | Live Streaming |
| Reliability         | High          | High          | Low (but fast) |

#### grpc

It provides a model for data to be converted to binary bytes for efficient transfer of data with lower data bytes.

![Screenshot_2025-06-04_at_12.19.14_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2025-06-04_at_12.19.14_PM.png)

Compatibility issues since binary bytes are harder to debug , browser incompatibility etc.

#### Timeouts and Retries with Backoff

![Screenshot_2025-06-04_at_4.50.47_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2025-06-04_at_4.50.47_PM.png)

Every request is expected to take certain amount of time to complete, if it takes longer we should give up and try again. This can be done by using timeouts.
But retries can also have its drawbacks if not done properly. Retrying again and again within same time intervals might not be effective since the system might need some time to recover.
One of the strategies for this is to apply exponential backoff. What it does is it increases the retry interval exponentially after every retry. This gives server the time to recover any faults that might have incurred.
Adding jitter(randomness) among the requests from different clients can also be helpful in retries. The worst case would be having all our failing requests synchronize and retry at the same time over.
One important note here is to ensure that APIs where retries are being applied are Idempotent to avoid any duplication.
Idempotent APIs are those APIs that produce the same output on every request. GET APIs are a great example for this. For POST however we can create a unique Idempotent key and use that to identify if the current request is already processed or processing.

#### Circuit Breakers

![Screenshot_2025-06-04_at_5.22.08_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2025-06-04_at_5.22.08_PM.png)

When a request goes through a bunch of services , say as per above diagram a failure or delay in response could propagate from service to service due to retries and take a service in the path down , say server B in our case.
This can be prevented by applying a circuit breaker. What is does is -

- It monitors for failures in calls to external services
- It stops the requests when the errors go beyond a certain limit and trips to Open state.
- Once is open state, all the requests fail
- After a certain time period , it moves to half-open state.
- A test request is sent to ensure the error is resolved and circuit moves to close state again.
