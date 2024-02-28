#satge1 using 
FROM python:3.9-alpine AS builder

WORKDIR /app/

COPY requirements.txt /app/

RUN apk update && \
    apk add --no-cache py3-pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["python","./setup.py"]


#satge2
FROM alpine:latest

WORKDIR /app/

COPY --from=builder /app/fabric_server/. ./
COPY fabric_server/. /app/


# Install Java and screen
RUN apk update && \
    apk add openjdk17 && \
    apk add screen

ENV JAVA_HOME=/usr/lib/jvm/default-jvm

CMD ["sh", "start.sh"]
