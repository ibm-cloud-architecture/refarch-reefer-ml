source ../scripts/setenv.sh NOSET
oc set env dc/reeferpredictivescoring KAFKA_BROKERS=$KAFKA_BROKERS
oc set env dc/reeferpredictivescoring KAFKA_ENV=$KAFKA_ENV
oc set env dc/reeferpredictivescoring KAFKA_APIKEY=$KAFKA_APIKEY
