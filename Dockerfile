# Stage 1: Build stage
FROM python:3.9-alpine AS builder

WORKDIR /app/

COPY requirements.txt /app/

RUN apk update && \
    apk add --no-cache py3-pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Run setup.py or any other build commands if needed
CMD ["python","./setup.py"]

# Stage 2: Final stage
FROM alpine:latest

WORKDIR /app/

COPY --from=builder /app/fabric_server/. ./
COPY fabric_server/. /app/

# Install Java, screen, and any other required packages
RUN apk update && \
    apk add openjdk17 && \
    apk add screen

ENV JAVA_HOME=/usr/lib/jvm/default-jvm
# Set the command to start the Minecraft server using screen
CMD ["sh", "start.sh"]
