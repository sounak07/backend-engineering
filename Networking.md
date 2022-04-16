# Networking

## Proxy vs Reverse Proxy

- A proxy allows clients to communicate (connect) with servers anonymously while a reverse proxy allows servers to communicate (serve) with clients anonymously. That's my one liner

### Proxy

- Server has no idea which client is connecting to server

![alt text](/resources/proxy1.png "RDS")

### Benifits
 - Anonymity
 - Caching
 - Blocking Unwanted sites
 - GeoFencing (Certain Clients can access certain servers based on region)

 ### Reverse Proxy

- Client has no idea which server he/she is connecting to server

![alt text](/resources/revProxy1.png "RDS")

### Benifits
 - Load balancing
 - Caching
 - Isolating internal traffice
 - Logging
 - Canary Deployment