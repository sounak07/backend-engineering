API Gateways act as a manager managing the incoming requests and routing them to their correct destination. Without API gateways clients with need to know the path to service they are requesting to which would make the entire architecture tightly coupled.
Think of API gateways as hotel front desk, directing them to the right set of people, without them guests will need to know the every hotel staff for a random request of a service. 
API gateways are relatively thin and simple tasks performing request, routing , authentication, caching etc. 
The evolution of API gateways parallels the microservice architecture since API gateway becomes essential for routing in a architecture involving many services.

Scaling an API gateways mostly involves few ways -
- Horizontal scaling, scaling out the servers since they are mostly stateless.
- Global distribution:
	- Using DNS based routing.
	- Using geoDNS to route users to the nearest gateway.
	- Config synchronisation across all gateways deployed across multiple regions.

API Gateways can also be configured to perform a bunch of other responsibilities. A request tracing via a API gateway involves the following -
- Request validation
- API Auth middlewares
- API routing to correct services
- Response transformations 
- Caching of response.

API Gateways are essential component for microservice architecture but might be a overkill for simple web apps and monoliths. 