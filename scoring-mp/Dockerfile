#########################################################################################
# This Dockerfile is mean for development purposes. For CI/CD use Dockerfile.multistage
# It is meant to be run after the application has been built using Maven
# It also expects:
# 1. The microprofile-config.properties file exists in src/main/resources/META-INF
# 2. The es-cert.jks truststore file to connect to Event Streams in OCP
#########################################################################################


FROM open-liberty:microProfile3-java11
LABEL maintainer="IBM Cloud Architecture Solution Engineering at IBM Cloud"

USER 1001
COPY target/starter-app.war /config/dropins
COPY src/main/liberty/config/server.xml /config
## The line below would copy the Event Streams truststore so that you can communicate with an Event Stream instance on OCP
COPY src/main/liberty/config/resources/security/es-cert.jks /config/resources/security/es-cert.jks

# Upgrade to production license if URL to JAR provided
ARG LICENSE_JAR_URL
RUN \
  if [ $LICENSE_JAR_URL ]; then \
    wget $LICENSE_JAR_URL -O /tmp/license.jar \
    && java -jar /tmp/license.jar -acceptLicense /opt/ibm \
    && rm /tmp/license.jar; \
  fi
