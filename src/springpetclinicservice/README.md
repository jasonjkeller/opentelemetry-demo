# Spring PetClinic

Runs the Spring PetClinic service: https://github.com/spring-projects/spring-petclinic

## Run

From the project root `opentelemetry-demo/` run: `docker-compose up`

If changes were made to any code then instead run the following to rebuild the images: `docker-compose up --build`

The Spring PetClinic service will be available at http://localhost:8087/.

## Load Generator

The Locust load generator file for Spring PetClinic is defined here:
`opentelemetry-demo/src/loadgenerator/locustfiles/springpetclinic-locustfile.py`
