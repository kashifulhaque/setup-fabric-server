# Stage 1: Build stage
FROM python:3.9-alpine AS builder

WORKDIR /app/

# Copy only requirements file to leverage Docker layer caching
COPY requirements.txt .

# Install required dependencies
RUN apk add --no-cache openjdk17 \
    && pip install --no-cache-dir -r requirements.txt

# Copy only necessary files for the application
COPY utils/ /app/utils/
COPY ./*.py /app/
COPY setup.py /app/


RUN python setup.py

# Stage 2: Final stage
FROM alpine:latest

WORKDIR /app/

COPY --from=builder /app/ .

# Install OpenJDK 17 and screen
RUN apk add --no-cache openjdk17 screen

ENV JAVA_HOME=/usr/lib/jvm/default-jvm

RUN chmod +x fabric_server/server.jar

# Set the command to start the Minecraft server using screen
CMD ["sh", "fabric_server/start.sh"]

