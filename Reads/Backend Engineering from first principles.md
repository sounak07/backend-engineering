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

![Screenshot_2025-11-30_at_12.05.14_AM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2025-11-30_at_12.05.14_AM.png)

Since origin and host in request are different if Allow-control-allow-origin is not sent or not same as origin(or *all origin) in request, response won't be allowed to go through. 

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

![Screenshot_2025-11-30_at_12.18.36_AM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2025-11-30_at_12.18.36_AM.png)

Allow-Max-age represents the time till this data is valid. If everything goes well the original request is completed.  Allow-Headers is something that server tells which headers are allowed. 

**HTTP Status Codes**

1XX - Information codes
3XX - Redirection codes (301 - Permanent redirect | 302 - Temp redirect | 304 - No change from last response, not modified ,used in cache)
2XX - Success (204 - Success but no content is return)
4XX - Client (400 |  401 |  404 | 403 - forbidden, users are auth but trying to access something restricted to them | 409 - Conflict , resource available)
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

![Screenshot_2025-11-30_at_3.45.06_PM](https://raw.githubusercontent.com/sounak07/backend-engineering/main/assets/Screenshot_2025-11-30_at_3.45.06_PM.png)

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

Authentication is WHO.

Modern Auth -
- OAuth
- JWT based
- Password Less
- Zero trust architecture 

**Sessions**
Sessions stores user related info which can be used to authenticate users when they make HTTP requests to certain resources to add/fetch data.
When a user authenticates themselves, a new session is created with user info and session info like session_id, expiry etc and are stored in some persistant storage like in a db or distributed cache. The session_id is then returned as cookie for the clients to be used for authorization without needing to authenticate everytime.
When the expiry time is over for a session , the server creates a new session updating the old one , sending a new cookie. This allows seemless distributed authorization throughout. 

Issues with Sessions - 
- Memory overhead became a major problem as we scale, storing the data of so many users became a major problem.
- With distributed architecture becoming mainstream, syncing the data throughout for all the systems introduced latency. 

**JWT**
JSON web tokens became quite popular to solve these above issues. Its a stateless way to authorise users releasing the server of the overhead of storing and managing sessions. 

JWT has 3 parts  - 
Headers - 

```
{
  "alg": "HS256" //hashing algo
  "type": "jwt"
}
```

Payload - Anything related to user data. 

```
{
  "iat":
  "id": 
  "name": 
  "role"

}
```

Signature 
The `secret-to-decode-encode` the data to generate the token.

This solved a bunch of issues around storage, scalability , statelessness. This allowed microservices to authenticate very seamlessly without needing to sync any data to get context. 
Also they are very portable, they can sent as cookies, stored in local storage or any else easily. 

There some problems too like token theft , Manual revocation of access became a problem and had to for them to expire. 

**Hybrid JWT**
Its a mix of stateless and stateful, extract the user data and check for its presence or maintain a list of blacklisted JWTs. But the questions remains why not just use sessions instead , they are more secure. So its a matter of debates and tradeoff. Using a auth provider can be a good choice around this to avoid these overheads.

**Cookie**
Cookie is a way to store certain info in client's browser which can used to authorise the users trying to access a server resource in all subsequent servers, say a auth token. Its easier to set cookies for the server since servers have access to browser cookies. 
An important thing to note is cookies are limited to a server, a cookie provided by one server can't be used by a different server. 

Stateful Auth - Session is stateful auth.
Stateless Auth - JWT , a signed token. 
API key -  Designed for machine to machine programmatic interactions 

##### 0Auth - 

OAuth is a protocol to delegate access. It allows resource owner(user) to grant services access to limited resources without needing to share user creds.

0Auth 1.0

![](https://miro.medium.com/v2/resize:fit:700/1*fACWJ6k07mTjLfermXFFPg.png)

In OAuth 1.0, the client receives an access token (and token secret) once after the user authorizes the app.  
For every subsequent API call, the client must generate a cryptographic signature using the consumer secret, token secret, and request data.  
The resource server re-calculates and verifies this signature on every request to ensure authenticity and integrity.  
The token itself is not re-issued on every request.

0Auth 2.0 

![](https://miro.medium.com/v2/resize:fit:700/1*hOycj214z21NsUKXdDzvGA.png)

0Auth 2.0 does not have these complexity, its uses HTTPS with bearer tokens to inform its identity. These doesn't need to be generated on every request but can have expiry. 

Open ID Connect

This is an extension of 0Auth 2.0 where the along with auth token an ID token is also issued which carries the identity of the resource owner. This allows clients to verify the resource owner's identify. It can also be used to get some basic resource owner info. 

|Feature|OAuth 1.0|OAuth 2.0|OAuth 2.0 + OIDC|
|---|---|---|---|
|Purpose|Authorization|Authorization|Identity + Authentication|
|Signing|Cryptographic signatures (complex)|No signatures (simpler), uses HTTPS|Same as OAuth 2.0, plus ID Token|
|Token Types|Access Token|Access Token|**ID Token + Access Token**|
|Identity/ Login?|❌ No|❌ No|✅ Yes (SSO login layer)|
|Security|Good but complex|Depends on TLS|Strong (with JWT ID Tokens)|
|Mobile-friendly|❌ Hard|✅ Yes|✅ Yes|

Single Sign-ON (SSO): 

SSO is a concept where the user signs into a central IDP (Identity provider) and the IDp provides Bearer token similar to 0Auth 2.0 to let the user sign in into multiple applications without having to sign in again. This is built on top of SAML and OIDC.

##### Authorisation

Authorisation is WHAT, what permissions this user has, what this user can do. 
A use case for this authorisation is Role based Access Control.
This allows the server to assign certain users specific roles that are different from others. 
Say some users are admin, some are just users etc. 
This is usually verified and assigned from configs stored in db or some other persistant storage. 

##### Error message and Timing Attacks

Friendly error messages can allow attackers to identify whats missing optimise their attack for success. Say if we prompt a message incorrect password, the attacker might know that username might be correct and password is wrong.
So avoiding friendly error messages is recommended. 

Timing attacks is another crucial concept in auth which allows attackers to time the requests to identify whats missing. 
Say if username is correct but password is wrong but for that comparison server needs to hash the password and compare with hashed stored pass, since hashing takes time , the difference in time could tell that password is where the request stopped. 
Using constant time responses or simulating delays in responses is recommended to avoid this. 

#### Validations and transformations

##### Types of validation

- Syntactic - Validations that checks where a string has a specific format or not. e.g. email has correct format or not
- Semantic - Checks if data makes sense, DOB cannot be in the future. Age of a person cannot be 365
- Type validation - Data type validation matching or not. 

##### Transformations

A way to transform the data in a way thats useful and accepted by the input layer without having to throw an error to the user. This is important because not always we have to ask user to correct the data, some data can be corrected on the server itself to save time and effort.

Say an email sent as SounAk@gmail.c is still valid, we can transform it in a suitable format of sounak@gmail.c and use it. 

#### Controllers, services and repositories

**Handlers/Controllers**
Each handler receives two objects - request and response. 
Once request object is received , the handler deserializes the data to its native data format, on failure of this we send a 400 to client. 
We do validations and transformations in this layer; all the HTTP related operations should also be limited to this layer.

**Service**
All the processing should be done by the service. The service should API agnostic, it shouldn't have any signatures of API, it should just be a processing layer.  A service call existing and process without calling a repository.

**Repository**
Mostly the layer that handles the database operations and is usually managed from the service layer. 

#### Middlewares and Request Contexts

**Middleware**

A middleware receives a request, response and a special function next from the runtime. Next is a function to pass the execution to the next middleware or execution function. Please know that middleware are intermediaries in the execution cycle and mostly not the end of them, but they surely end a request and send a response back if they choose to. 

Middlewares are basically a way to run some logic for every API request a server receives. They are like functions. Without them we would have to duplicate the logic in every handler or call a function in every handler. Middlewares allow us to avoid that. 

Middlewares can be used for security checks like auth token checks, add some context to the request objects(add some headers), loggers , rate limit checks,  etc. 
Global error handlers are also a major usecase of middlewares, even compressions can be done with middlewares.

**Request Context**

Request context carries the metadata of a particular request which can be used as a state by the sequent handlers or middlewares to make certain decisions. Say user data after auth can be stored there. Request id can also be stored in the context, this acts as unique id throughout the request to trace the request. 
Its safer to extract and store user id from auth token as this way we are not allowing attackers to use the request data to get info of other users by injecting user ids of non authenticated users. 

#### API Design 

Tim berners lee invented the WWW; initial HTTP, browsers, web server, web browser. 
Roy fielding was the architecture of the web, introducing client-server-isolating each block to evolve on its own. 
He also introduced uniform interface ,cache, making request stateless , code on demand (js executables in client)

##### Idempotency 

The outcome and the side effects of an API request no matter how many times its called should remain the same. Say if somebody has paid for a service online, they should not be paying it again. 

A **GET** request is always idempotent-it will always return some data in a specific format. 
**PATCH**(partial update) and **PUT**(Complete replacement) are also idempotent since the outcome is updating of data not really creating anything new and state remains same.
**DELETE** is also idempotent since the outcome is removing some data no matter what. 
**POST** however is not idempotent since its creating something new to its actually changing the state.
**POST** can be a universal method for actions that don't fall in any other method, say /send-email. 

##### Designing API Interface

After going through figma wireframes, we need to design db schemas and finally we come API interfaces. 

**Principles of Designing REST APIs**

- While designing an API which is about getting/creating/updating a book, we should use /books not /book since the resource itself is not a singular entity. 
- Not adding spaces in urls, instead use slugs-a human readable representation of a property of a resource. Say - DHL US -> dhl_us/dhl-us
- Pagination in APIs should have some params like limit, page and total which represents the number of data we want from data, which the portion of data we want and total data present respectively. 
- Sorting should also be supported in the list APIs
- APIs should have some sane defaults, also should have checks for unreasonable  values passed for defaults.
- A custom action API should use POST and the API structure for a clone API should look like `{base}/projects/{id}/clone` 

#### References

[Medium](https://medium.com/identity-beyond-borders/oauth-1-0-vs-oauth-2-0-e36f8924a835)
[Youtube Playlist](https://www.youtube.com/playlist?list=PLui3EUkuMTPgZcV0QhQrOcwMPcBCcd_Q1)


