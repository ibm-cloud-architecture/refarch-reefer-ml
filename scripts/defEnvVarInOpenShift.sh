source ./setenv.sh $1
oc set env dc/reefersimulator KAFKA_BROKERS=$KAFKA_BROKERS
oc set env dc/reefersimulator KAFKA_ENV=$KAFKA_ENV
oc set env dc/reefersimulator KAFKA_APIKEY=$KAFKA_APIKEY