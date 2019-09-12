source ../scripts/setenv.sh

docker run -p 8080:8080 -e KAFKA_ENV=$KAFKA_ENV \
    -e KAFKA_BROKERS=$KAFKA_BROKERS \
    -e KAFKA_APIKEY=$KAFKA_APIKEY \
    ibmcase/reefersimulator