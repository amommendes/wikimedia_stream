#!/bin/bash

C_GREEN='\e[32m'
C_RED='\e[31m'
C_ORANGE='\e[33m'
C_CYAN='\e[35m'
C_WHITE='\e[37m'
C_NONE='\e[0m'

info=" ${C_GREEN} [INFO] ${C_NONE}"
error=" ${C_RED} [ERROR] ${C_WHITE}"
unset build

declare -r parameters=$#
if [[ "${parameters}" == 0 ]]; then echo "Usage: sh build.sh -b [TRUE | FALSE]" && exit 1 ; fi

while getopts ":b:" opt ; do
    case "$opt" in
        b ) # Get Cluster Name
            build="$OPTARG"
            ;;
        * ) # Print usage
           echo "Usage: sh build.sh -b [TRUE | FALSE]"
           exit 1
            ;;
    esac
done


echo -e $(date) ${info}Starting Dashboard Application
cp -rf app docker/dashboard/
cp requirements.txt docker/dashboard/
echo -e $(date) ${info}Artifacts copied to build directory

cd docker

echo -e $(date) ${info}Stopping Services

docker-compose stop



if [[ "${build}" == "TRUE" ]]; then 
    echo -e $(date) ${info}Building Containers with docker-compose build
    docker-compose build
    rc=$?
    if [ "${rc}" -eq "0" ]; then
        echo -e $(date) ${info}Containers Built
    else
        echo $(date) ${error}Error while building containers
        exit 1
    fi
fi

echo -e $(date) ${info} Starting Services:
echo -e $(date) ${info} Starting Elasticsearch Service
docker-compose up -d elasticsearch
sleep 60

echo -e $(date) ${info} Starting Kibana Service
docker-compose up -d kibana
sleep 60

echo -e $(date) ${info} Starting Dashboard Service
docker-compose up -d dashboard

rc=$?

if [ "${rc}" -eq "0" ]; then
    echo -e $(date) ${info} Containers started
else
    echo $(date) ${error} Error while starting containers
    exit 1
fi
exit 0