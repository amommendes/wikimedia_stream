#!/bin/bash

echo $(date) [INFO] Building Application
cp -r app docker/dashboard/
cp requirements.txt docker/dashboard/
echo $(date) [INFO] Artifacts copied to build directory

cd docker

echo $(date) [INFO] Building Containers

docker-compose build

rc=$?

if [ "${rc}" -eq "0" ]; then
    echo $(date) [INFO] Building Containers
else
    echo $(date) [Error] Error while building containers
    exit 1
fi

echo $(date) [INFO] Starting containers
echo $(date) [INFO] Starting Elasticsearch
docker-compose up -d elasticsearch
sleep 60

echo $(date) [INFO] Starting Kibana
docker-compose up -d kibana
sleep 60

echo $(date) [INFO] Starting Dashboard
docker-compose up -d dashboard

rc=$?

if [ "${rc}" -eq "0" ]; then
    echo $(date) [INFO] Containers started
else
    echo $(date) [Error] Error while starting containers
    exit 1
fi
exit 0