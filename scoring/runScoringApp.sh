#!/bin/bash
source ../scripts/setenv.sh NOSET
docker run -e KAFKA_BROKERS=$KAFKA_BROKERS -e KAFKA_APIKEY=$KAFKA_APIKEY -e KAFKA_ENV=$KAFKA_ENV -v $(pwd)/..:/home -ti ibmcase/python bash -c "cd /home/scoring && export PYTHONPATH=/home && python ScoringApp.py"