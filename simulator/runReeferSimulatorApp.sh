if [[ $# -ne 1 ]]
then
    echo "Usage: runReeferSimulatorApp.sh [LOCAL | IBMCLOUD]"
    exit 1
fi
source ../scripts/setenv.sh $1 NOSET

if [[ -z "$DOCKER_NET" ]]
then
    docker run -p 8080:8080 -e KAFKA_ENV=$KAFKA_ENV \
    -e KAFKA_BROKERS=$KAFKA_BROKERS \
    -network $DOCKER_NET \
    -e KAFKA_APIKEY=$KAFKA_APIKEY \
    ibmcase/reefersimulator
else
    docker run -p 8080:8080 -e KAFKA_ENV=$KAFKA_ENV \
    -e KAFKA_BROKERS=$KAFKA_BROKERS \
    -e KAFKA_APIKEY=$KAFKA_APIKEY \
    ibmcase/reefersimulator
fi