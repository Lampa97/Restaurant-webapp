FROM python:3.12-slim

WORKDIR /code

RUN apt-get update \
    && apt-get install -y gcc libpq-dev libjpeg-dev zlib1g-dev curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . .
