Machines do not go by names like we humans do. They go by numbers or IPs like ***192.168.1.1***, ***192.168.1.2***, ***192.168.1.3***
But we humans we cannot really remember these numbers.

Imagine how many phone numbers of friends do you have in mind right now as opposed to their names.
Why ? 
Because for humans it easier to remember names then numbers. In order to bridge this Gap between humans and Machines we use the DNS.

DNS primarily resolves the Names with numbers or rather domain names with IPs to be precise. 

So what happens when we type in an web address on a domain name into the browser say yahoo.com ?

We don't necessarily have to type in the domain, we can just type the IP address and get the response back if we know it, but as I explained before it would be very hard for us to remember IP addresses. 

So when we type in the domain name at first the browser looks in its cache to resolve the name, then it sends the request to the OS, OS does the same and looks in OS's DNS cache and if nothing in found , it goes to the next level which is the **DNS Resolver** .

If nothing is found in the DNS resolver cache it directs itself to one the **DNS Root servers**.

Now what are **DNS Root servers** ??

The root servers are at the top of the hierarchy of the DNS. There are 13 sets of these root servers placed strategically across the world and are operated by 12 different Orgs.

How does the Resolver know the IP of the root servers since they are at the Top of hierarchy right ?

Well Every resolver maintains the list of those 13 sets of IPs in order to solve this problem.

How does the DNS resolver decide which root server to send the request to out of the 13 ?

When a DNS resolver receives a request, it consults a list of 13 root DNS servers. It can use methods like round-robin, random selection, or consider factors like proximity and performance to choose which root server to query. This helps distribute the load and optimise response times. Additionally, administrators can configure preferences for specific root servers.

The root server is not going to know the IP address of the domain is, it will direct the **DNS Resolver** to one the **TLD servers**.

What is a TLD server ??

TLD or Top-level Domain servers maintain a group of domains that share a common domain extension such as .com, .net, .co, .io etc or the top level domains.
Think of it as a section of a library which stores a particular type of books.

There are usually two types of TLD servers out there -
Generic -  .com. .co, .io
Country Code - .uk, .us, .in 

In our case the Root server will direct the Resolver to the .com TLD server.
So what does TLD server do now ?
The TLD does not know the IP of yahoo.com, what it will do is it will direct the Resolver to another server called the **Authoritative name servers.**

**Authoritative name servers** are responsible for storing every information of the domain including the IP, they are the final authority. 

So once the **Authoritative name servers** sends back the resolver the IP address it will send back the IP to the Browser or the OS and we should be reach yahoo.com, finally. 

The Resolver will also store the IP in its cache in order to avoid all these steps the next time it has the same query.


