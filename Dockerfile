FROM alpine:latest AS builder

WORKDIR /app/
# me making unstable code even worse (thumbs up emoji)

RUN apk update && \
    apk add python3 py3-pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --break-system-packages
RUN mkdir -p /app/utils && mkdir -p /app/fabric_server
COPY utils/. /app/utils
COPY . /app/fabric_server
CMD ["python3" , "setup.py"]

FROM alpine:latest

WORKDIR /app/
RUN mkdir -p /app/fabric_server
COPY --from=builder /app/fabric_server/ /app/fabric_server/

RUN apk update && \
    apk add openjdk17 && \
    apk add screen

ENV JAVA_HOME=/usr/lib/jvm/default-jvm
RUN chmod 755 /app/fabric_server/setup.sh

#CMD ["sh", "/app/fabric_server/setup.sh"]
