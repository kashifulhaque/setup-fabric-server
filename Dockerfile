FROM alpine:latest

WORKDIR /app/

# Copy the entire contents of the 'fabric_server' directory into the container
COPY fabric_server/. /app/

# Install Java and screen
RUN apk update && \
    apk add openjdk17 && \
    apk add screen

# Set environment variable for Java home
ENV JAVA_HOME=/usr/lib/jvm/default-jvm

# Specify the command to run when the container starts
CMD ["sh", "start.sh"]
