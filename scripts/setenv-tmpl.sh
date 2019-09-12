export KAFKA_BROKERS=broker-3....
export KAFKA_APIKEY=""
export KAFKA_ENV=LOCAL or IBMCLOUD or ICP
if [[ $# -eq 1 ]]
then
    oc set env dc/reefersimulator KAFKA_BROKERS=$KAFKA_BROKERS
    oc set env dc/reefersimulator KAFKA_ENV=$KAFKA_ENV
    oc set env dc/reefersimulator KAFKA_APIKEY=$KAFKA_APIKEY
fi


