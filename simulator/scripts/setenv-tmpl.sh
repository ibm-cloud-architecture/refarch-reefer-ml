export KAFKA_BROKERS=broker-3-1fz6f8v6q69xp392.kafka.svc01.us-south.eventstreams.cloud.ibm.com:9093,broker-1-1fz6f8v6q69xp392.kafka.svc01.us-south.eventstreams.cloud.ibm.com:9093,broker-0-1fz6f8v6q69xp392.kafka.svc01.us-south.eventstreams.cloud.ibm.com:9093,broker-5-1fz6f8v6q69xp392.kafka.svc01.us-south.eventstreams.cloud.ibm.com:9093,broker-2-1fz6f8v6q69xp392.kafka.svc01.us-south.eventstreams.cloud.ibm.com:9093,broker-4-1fz6f8v6q69xp392.kafka.svc01.us-south.eventstreams.cloud.ibm.com:9093
export KAFKA_APIKEY=""
export KAFKA_ENV=IBMCLOUD

if [[ $# -eq 1 ]]
then
    if [[ "$1" != "NOSET" ]]
    then
        if [[ "$KAFKA_ENV" == "IBMCLOUD" ]]
        then
            oc set env dc/order-producer-python KAFKA_BROKERS=$KAFKA_BROKERS
            oc set env dc/order-producer-python KAFKA_ENV=$KAFKA_ENV
            oc set env dc/order-producer-python KAFKA_APIKEY=$KAFKA_APIKEY
        fi
    fi
fi


