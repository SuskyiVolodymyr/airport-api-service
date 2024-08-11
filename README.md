# Airport API Service
This project is an API service designed to manage various aspects of an airport's operations. The API includes endpoints for managing countries, airports, routes, airplane types, airplanes (with images), crew members, flights, and orders.

## Endpoints
- Countries: Retrieve a list of countries or a specific country.
- Airports: Retrieve a list of airports or a specific airport.
- Routes: Retrieve a list of routes or a specific route.
- Airplane Types: Retrieve a list of airplane types or a specific airplane type.
- Airplanes: Retrieve a list of airplanes or a specific airplane, along with associated images.
- Crew Members: Retrieve a list of crew members or a specific crew member.
- Flights: Retrieve a list of flights or a specific flight.
- Orders: Retrieve a list of orders, a specific order, or create tickets within an order.

### Api documentation
You can access the API documentation via the Swagger UI at the following endpoint:
- Swagger UI: `/api/doc/swagger`
## User Permissions
Users can perform GET requests to retrieve lists or specific items for all the above endpoints, except for the Orders endpoint, where users also have the ability to create tickets.

## Docker Setup
This project is containerized using Docker. To run the project, follow these steps:

### How to Run
- Copy the sample environment file and populate it with the required data
- Build and start the Docker containers:
`docker-compose up --build`
- Create admin user