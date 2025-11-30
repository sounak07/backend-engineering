## Backend Engineering from first principles

#### Frontend vs Backend

Backend processes the requests in the servers based on the I/O and returns the response. The entire processing is happening in the servers.

Frontend however fetches all the code from the servers and run them in the browser itself, basically it acts as a runtime for the code. The is done in sandbox environment.
Thats why browsers have a lot of security policies like **CORS** which does not allow the code to call external API that have a different domain than the current one.
This important to avoid running malicious remote code executing commands in local machine.

**Why can't we run backend logic in FE ?**

- Security reasons
- CORS not allowing external APIs
- Browsers cannot connect to databases efficiently since browsers are not designed to run database drivers efficiently. They cannot maintain connection pooling, socket connections, handle binary data. Each user would need to create a separate connection which will overwhelm the db servers.
- FE environments vary can vary from user to user, the resources might not be enough to run commute heavy, or high memory usage tasks and devs cannot scale or change it.

**Why learning backend using first principles helps**

When you learn backend fundamentals—not just frameworks—you start seeing the **bigger picture**.

You’re no longer learning tools…  
You’re learning **concepts, patterns, and mental models** that transfer across every language and stack.

This shift changes everything:

🔹 You recognize architectural patterns instantly  
🔹 You onboard into new projects, tools, and languages _much faster_  
🔹 You contribute earlier and with more confidence  
🔹 You avoid “syntax fatigue” because you know what truly matters  
🔹 You choose the right tool for the job, not the one you happen to know  
🔹 You become someone who can **solve problems**, not just someone who knows a tool

Learning from first principles makes you **adaptable, valuable, and future-proof**.  
Tools change. Ecosystems evolve.  
But strong fundamentals compound forever.

#### HTTP

- Its stateless
- It implements client server model

Types of headers -

- Request headers - User-agent, Authorisations, cookie, accept (type of content)
- General headers
- Representation headers
- Security headers

**Idempotent vs Non-idempotent in HTTP methods -**
Idempotent - GET, PUT, DELETE
Non-Idempotent - POST

**OPTIONS HTTP Method {CORS}** -

Used to fetch server capabilities CORS(Cross origin Requests)

CORS lets the browsers control how the webapps interact with resources that are hosted in different domains(cross origin).
CORS allow servers to specify who can access their specific resources.
Without proper CORS browsers wont allow webapps to request resources from host that are different from origin host.
Say For example.com, api.example.com won't be allowed if CORS specifying that is not set.

When ever the browser sends a request ,

![alt text](https://raw.githubusercontent.com/sounak07/backend-engineering/main/resources/Screenshot%202025-11-30%20at%2012.05.14%20AM.png)

Since origin and host in request are different if Allow-control-allow-origin is not sent or not same as origin(or \*all origin) in request, response won't be allowed to go through.

Now there can be 2 types of request -

- Simple request
- Preflighted request

A simple request is a regular request.
A pre-flighted request needs to fetch some data before the actual request is made.

To qualify for preflighted requests there are certain conditions :

- It should be PUT/DELETE
- content type should be anything other than application/form-encoded, multipart-form, text/plain
- Should include headers other than general headers like auth, x-custom-header etc

A pre-flighted request make an OPTIONS request to get the CORS to check the cross origin support details for the request ahead. If proper CORS are not returned request is blocked.
If it does it returns the following response.

![alt text](https://raw.githubusercontent.com/sounak07/backend-engineering/main/resources/Screenshot%202025-11-30%20at%2012.18.36%20AM.png)

Allow-Max-age represents the time till this data is valid. If everything goes well the original request is completed. Allow-Headers is something that server tells which headers are allowed.

**HTTP Status Codes**

1XX - Information codes
3XX - Redirection codes (301 - Permanent redirect | 302 - Temp redirect | 304 - No change from last response, not modified ,used in cache)
2XX - Success (204 - Success but no content is return)
4XX - Client (400 | 401 | 404 | 403 - forbidden, users are auth but trying to access something restricted to them | 409 - Conflict , resource available)
5XX - Server (502 - bad gateway, upstream server returned invalid response, returned by reverse proxies | 503 - Service is down | 504 - Gateway timeout, upstream server timed out )

**HTTP Caching**

We can cache a request response using the HTTP headers like ETag, If-modified-since, If-None-Match.

Say we did a update PUT request, server would send a ETag, which is we can use an identifier during GET requests.
If the client sends ETag that matches with the one provided during update and If-modified-since satisfies did not surpass the time resource was modified we get a 304(not Modified).
If the Etag does not match , the server sends the updated ETag with last modified and the cycle goes on.
This isn't really used extensively after client caching with react, angular started becoming mainstream but can be still used for simple caching.

##### Content Negotiations

Content negotiations allow HTTP to specify details like language , type of data(json/xml/text) using HTTP headers like -
`Accept-language`, `Accept`, `Accept-encoding` etc.

HTTP compression is one important concept. It allows the browser to decompress compressed data sent from the server hence serving same output but reducing the size of data sent via network.
`Accept-encoding` is the header which can be used to specify the types of encoding the browser supports, so server can send data encoded in say gzip.

##### Handling large files

**Sending data**

Sending large files to server is usually done by using Content-type = Multipart/form-data.
Since in this case data is sent in parts, client need to add a delimiter to specify the start and end of the data. That delimiter is specified within Content-type as

```
Content-type : multipart/form-data; boundary=-----<some_identifier>
```

**Receiving Data**

![alt text](https://raw.githubusercontent.com/sounak07/backend-engineering/main/resources/Screenshot%202025-11-30%20at%203.45.06%20PM.png)

Streaming the data back to the client is a good way to send large data. If we check the Content-type of the response its `Content-type: text/event-stream` which is done keeping the connection alive using `Connection: keep-alive`

##### HTTPS (SSL, TLS)

SSL - Protocol to encrypt the data sent over the network.
TLS - Upgrade version of SSL which uses certificates establish authentication for encryption and decryption btw client and server.
HTTPS - Secure encrypted version of HTTP which implements TLS.

#### Serialization vs De-serialization

The data-types of client and server can be very different.
Say Client is written is js and server is in python, How does the server reconcile the data received from client written in js, the data types are completely different right?

This is where Serialization and De-serialization comes in.
Serialization is basically converting the data to a standard format which is language or data type agnostic so that anyone with right access can understand the data sent or received.

**Serialization Standards**

- Text Format
  - JSON (JS object notation)
  - YAML
  - XML
- Binary format
  - Protobuff
  - Avro

#### Authentication and Authorization
