#!/bin/bash

set -e

docker build -f Dockerfile-Base -t docker-pipeline-base .
docker build -f Dockerfile-End -t docker-pipeline-end .
docker build -f Dockerfile-Source -t docker-pipeline-source .
docker build -f Dockerfile-Worker -t docker-pipeline-worker .