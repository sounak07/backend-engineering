[Blog](https://blog.bytebytego.com/p/everything-you-always-wanted-to-know) [Implementation](https://github.com/sounak07/systems_and_designs/tree/main/TCP)

1. TCP is Connection Oriented , means it establishes a connection between two specific servers.
2. TCP is reliable. TCP guarantees the delivery of the segments, no matter what the network condition is.
3. TCP is bitstream-oriented. With TCP, application layer data is segmented. The transport layer remains oblivious to the boundary of a message. In addition, the segments must be processed sequentially, and duplicated segments are discarded.

![TCP](https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F30a07a70-c0dd-4e5e-b949-042c7368cc39_1600x934.png)

- **Sequence Number -**  In TCP application layer data is segmented. Then each segment is assigned a random 32-bit value is assigned as the initial sequence number. The receiving end uses this sequence number to send back an acknowledgment. The sequence number serves as a mechanism to ensure sequential processing of the segments at the receiving end.

- **Acknowledgment number -**  This 32-bit number is used by the receiver to request the next TCP segment. This value is the sequence number incremented by one. When the sender receives this acknowledgment, it can assume that all preceding data has been received successfully. This mechanism works to prevent any data losses.

- **Flags -** Control bits which tells whether the message is for establishing a connection, transmitting data, or terminating a connection.
   - ACK - Used for acknowledgments.
   - RST - Used to reset the connection when there are irrecoverable errors.
   - SYN - Used for the initial 3-way handshake. The sequence number field must be set.
   - FIN - Used to terminate the connection.



## The 3 Way Handshake

![TCP Header](https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F781159a5-f60e-4c94-b815-c8abd8d73b12_1600x1442.png)




## The 4 way Handshake (Closing a TCP)

![img](https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e386fb3-7fc6-477a-aa50-c314a462a349_1600x1591.png)



### How do we know if server/client is alive after connection is Established ?

A solution called *keepalive* is used to tackle this problem. When connection is established , a timer is set if keepalive is active. When the timer expires server sends **ACK probe without data.** 
Even after several consecutive probe segments are sent without any response from the client, the server presumes the TCP connection is dead.


### Some scenarios of TCP Keepalive

1. The client is functioning normally. The server sends a keepalive probe and receives a reply. The keepalive timer resets, and the server will send the next probe when the timer expires again.

2. The client process is down. The operating system on the client side sends a FIN segment to the server when it reclaims process resources. 

3. The client machine goes offline and restarts. As the diagram below shows, when the client comes back online, it has no knowledge of the previous connection. When the server attempts to send data to the client over this dead connection, the client replies with an **RST** segment, which forces the server to close the connection.

4. The client's machine goes offline and doesn’t recover. We’ve talked about this scenario - after several unanswered probes, the server considers the connection as dead.


 
 
