FROM ubuntu:latest AS builder

WORKDIR /app/

RUN apt-get update && \
    apt-get install -y python3 python3-pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY utils/. /app/utils

CMD ["python3" , "setup.py"]

FROM alpine:latest

WORKDIR /app/

COPY --from=builder /app/fabric_server/ /app/fabric_server/

RUN apk update && \
    apk add openjdk17 && \
    apk add screen

ENV JAVA_HOME=/usr/lib/jvm/default-jvm

CMD ["sh", "start.sh"]
