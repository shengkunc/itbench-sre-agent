FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/itbench-sre-agent && \
    chgrp -R 0 /app && \
    chmod -R g=u /app

RUN pip install --no-cache-dir uv
RUN pip install --no-cache-dir crewai==0.95.0
RUN pip install --no-cache-dir crewai-tools
RUN crewai install

WORKDIR /app/itbench-sre-agent
COPY . .

RUN chgrp -R 0 /app && \
    chmod -R g=u /app

USER 1001
