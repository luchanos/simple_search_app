ARG BASE_IMAGE=python:3.9.12
FROM $BASE_IMAGE

# system update & package install
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

RUN apt-get -y update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    openssl libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .
WORKDIR .

# pip & poetry
RUN python3 -m pip install --user --upgrade pip && \
    python3 -m pip install -r requirements.txt

# Configration
EXPOSE 8000

# Execute
CMD ["yoyo apply --database postgresql://postgres:postgres@db:5432/postgres ../migrations -b"]
CMD ["python", "main.py"]
# yoyo apply --database postgresql://postgres:postgres@db:5432/postgres ../migrations -b
# yoyo apply --database postgresql://postgres:postgres@0.0.0.0:5432/postgres ../migrations -b