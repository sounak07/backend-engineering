## How Khan Academy Scaled to 30 Million Users


##### Simple and Stupid 

Khan academy served their content from youtube for simplicity. They used Amazon S3 with Fastly CDN as a fallback and for regions where Youtube was not allowed. S3 would store the videos and Fastly will cache them for subsequent views.

They used a Content Management system with versioned control store. Its used to track and display the dynamic behaviour of content  to track the progress of students, watch times, completion rate etc. 

##### Architecture Evolution 

Khan Academy started of with a monolith architecture but shifted to micro-services as they scaled for various reasons like -
- Easy to optimise for perf and cost 
- Easy to deploy, run tests and optimize individual services.
- Reduce blast radius of deployment

Each service is responsible for its own data and can talk to each other only via GraphQL API.

##### Don't Reinvent the wheel 

Instead of buying more resources for scaling they used Google cloud serverless engine to run their services and focused more on the application code thus avoiding reinventing the wheel.

##### Right Tools

After starting with Python they eventually moved to Go for better build times, lower memory consumption and concurrency. This enabled better performance at a lower cost.
Besides they used Google cloud datastore , which is a managed NoSQL database from Google cloud. Offloading scaling to google they focused more on the educational content creation. 

##### No Repetitions 

To enhance performance and scalability they cached static data. All the traffic was directed through Fastly to avoid unnecessary load on the servers. They also cached common queries , user preferences , sessions etc using memcache. 

##### Communication

They maintained an effective communication among teams by discussing design choices. They used something called ADR(Architecture Decision Records) to communicate design changes. 
ADR is document about how a system is designed. 



[Reference](https://newsletter.systemdesign.one/p/khan-academy-architecture)