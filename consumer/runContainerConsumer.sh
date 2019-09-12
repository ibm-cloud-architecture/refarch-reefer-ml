#!/bin/bash
if [[ $# -ne 2 ]]
then
    echo "Usage: runContainConsumer.sh [LOCAL | IBMCLOUD] containerid"
    exit 1
fi
source ../scripts/setenv.sh $1 NOSET

if [[ -z "$DOCKER_NET" ]]
then
    docker run -e KAFKA_BROKERS=$KAFKA_BROKERS \
    -network $DOCKER_NET \
    -e KAFKA_APIKEY=$KAFKA_APIKEY \
    -e KAFKA_ENV=$KAFKA_ENV \
    -ti ibmcase/containerconsumer \
    bash -c "export PYTHONPATH=/server && python TraceContainerEventsApp.py $2"

else
    docker run -e KAFKA_BROKERS=$KAFKA_BROKERS \
    -e KAFKA_APIKEY=$KAFKA_APIKEY \
    -e KAFKA_ENV=$KAFKA_ENV \
    -ti ibmcase/containerconsumer \
    bash -c "export PYTHONPATH=/server && python TraceContainerEventsApp.py $2"
fi