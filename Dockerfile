FROM alpine:latest

WORKDIR /app/

COPY fabric_server/. /app/

# Install Java and screen
RUN apk update && \
    apk add openjdk17 && \
    apk add screen

# Set environment variable for Java home
ENV JAVA_HOME=/usr/lib/jvm/default-jvm

CMD ["sh", "start.sh"]
