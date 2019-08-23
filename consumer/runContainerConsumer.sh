#!/bin/bash
if [[ $# -eq 0 ]];then
    cid="C02"
else
    cid=$1
fi
source ../scripts/setenv.sh NOSET
docker run -e KAFKA_BROKERS=$KAFKA_BROKERS -e KAFKA_APIKEY=$KAFKA_APIKEY -e KAFKA_ENV=$KAFKA_ENV -v $(pwd)/..:/home --network=docker_default -ti ibmcase/python bash -c "cd /home/ContainersPython && export PYTHONPATH=/home && python ConsumeContainers.py $cid"