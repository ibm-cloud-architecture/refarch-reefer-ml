#!/usr/bin/env bash

# Script we are executing
echo -e " \e[32m@@@ Excuting script: \e[1;33maddContainer.sh \e[0m"

## Variables

KAFKA_BROKERS=""
KAFKA_APIKEY=""
CA_LOCATION=""
PEM_FILE=""

# Read arguments
if [[ $# -ne 3 ]];then
    echo "Not enough arguments have been provided for the producer. Using the defaults:"
    echo "- Kafka environment --> LOCAL"
    echo "- Kafka topic name --> containers"
    echo "- Container ID --> c_1"
    kcenv=LOCAL
    cid="c_1"
    topic_name="containers"
else
    echo "Producer values:"
    echo "- Kafka environment --> $1"
    echo "- Kafka topic name --> $3"
    echo "- Container ID --> $2"
    kcenv=$1
    cid=$2
    topic_name=$3
fi

# Check if the ibmcase/python docker image exists
EXISTS="$(docker images | awk '{print $1 ":" $2}' | grep ibmcase-python:test)"
if [ -z "${EXISTS}" ]
then
    echo -e "The ibmcase/python docker image does not exist. Creating such image..."
    docker build -f docker-python-tools -t ibmcase-python:test .
fi

if [ "OCP" == "${kcenv}" ]; then
    add_cert_to_container_command=" -e PEM_CERT=/certs/${PEM_FILE} -v ${CA_LOCATION}:/certs"
fi
if [ "LOCAL" == "${kcenv}" ]; then
    attach_to_network="--network=docker_default"
fi

# Run the container producer
# We are running the ProduceContainer.py python script into a python enabled container
# Attached to the same docker_default docker network as the other components
# We also pass to the python producer the Container ID we want to produce
docker run  -e KAFKA_BROKERS=$KAFKA_BROKERS \
            -e KAFKA_APIKEY=$KAFKA_APIKEY \
            -e KAFKA_ENV=$kcenv \
            ${add_cert_to_container_command} \
            ${attach_to_network} \
            -v ${PWD}:/tmp/test \
            --rm \
            -ti ibmcase-python:test bash \
            -c "cd /tmp/test && \
                export PYTHONPATH=\${PYTHONPATH}:/tmp/tests && \
                python ProduceContainer.py $cid $topic_name"
