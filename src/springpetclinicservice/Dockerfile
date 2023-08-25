FROM eclipse-temurin:17-jdk AS petclinic-builder

RUN apt update && apt upgrade -y && apt install -y git

WORKDIR /root/

RUN git clone https://github.com/spring-projects/spring-petclinic.git
WORKDIR /root/spring-petclinic/
RUN ./mvnw -Dmaven.test.skip package

# -----------------------------------------------------------------------------

FROM eclipse-temurin:17

ARG version=1.28.0
WORKDIR /root/

COPY --from=petclinic-builder /root/spring-petclinic/target/spring-petclinic*.jar ./
ADD https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/download/v$version/opentelemetry-javaagent.jar /root/opentelemetry-javaagent.jar
ENV JAVA_TOOL_OPTIONS="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005 -javaagent:/root/opentelemetry-javaagent.jar"

EXPOSE ${SPRING_PETCLINIC_SERVICE_PORT}
CMD ${JAVA_HOME}/bin/java -Xdebug -Dserver.port=${SPRING_PETCLINIC_SERVICE_PORT} -Djava.security.egd=file:/dev/./urandom -jar /root/spring-petclinic*.jar
#TODO setup MySql and use -Dspring.profiles.active=mysql
