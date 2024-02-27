# Use Alpine Linux as the base image
FROM python:3.9-alpine


WORKDIR /app/

COPY requirements.txt /app/

# Install dependencies
RUN apk update

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["python3", "./setup.py"]
