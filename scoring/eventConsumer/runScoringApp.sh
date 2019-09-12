#!/bin/bash
if [[ $# -ne 1 ]]
then
    echo "Usage: runScoringApp.sh [LOCAL | IBMCLOUD]"
    exit 1
fi
source ../../scripts/setenv.sh $1 NOSET

if [[ -z "$DOCKER_NET" ]]
then
   docker run -network $DOCKER_NET -e KAFKA_BROKERS=$KAFKA_BROKERS -e KAFKA_APIKEY=$KAFKA_APIKEY -e KAFKA_ENV=$KAFKA_ENV ibmcase/predictivescoring
else
   docker run -e KAFKA_BROKERS=$KAFKA_BROKERS -e KAFKA_APIKEY=$KAFKA_APIKEY -e KAFKA_ENV=$KAFKA_ENV ibmcase/predictivescoring 
   
fi