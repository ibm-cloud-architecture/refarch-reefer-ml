#!/bin/bash
if [[ $# -ne 1 ]];then
 echo "Usage createPGtables.sh [LOCAL  | IBMCLOUD ]"
 exit 1
fi

source ./setenv.sh $1

docker run -v $(pwd):/home -e KAFKA_BROKERS=$KAFKA_BROKERS \
     -e KAFKA_APIKEY=$KAFKA_APIKEY \
     -e KAFKA_ENV=$KAFKA_ENV  \
     -e POSTGRESQL_URL=$POSTGRES_URL \
     --network docker_default\
     -e POSTGRES_DBNANE=$POSTGRES_DBNANE \
     -e POSTGRES_SSL_PEM=$POSTGRES_SSL_PEM\
     -ti ibmcase/python bash -c "python simulator/infrastructure/ReeferRepository.py"