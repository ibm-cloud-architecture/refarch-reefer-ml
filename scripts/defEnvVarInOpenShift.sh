source ./setenv.sh $1
oc set env dc/reefersimulator KAFKA_BROKERS=$KAFKA_BROKERS
oc set env dc/reefersimulator KAFKA_APIKEY=$KAFKA_APIKEY
oc set env dc/reefersimulator KAFKA_CERT=/opt/app-root/src/es-cert.pem
oc set env dc/reeferpredictivescoring KAFKA_BROKERS=$KAFKA_BROKERS
oc set env dc/reeferpredictivescoring KAFKA_APIKEY=$KAFKA_APIKEY
oc set env dc/reeferpredictivescoring KAFKA_CERT=/opt/app-root/src/es-cert.pem
oc set env dc/reefercontainermaintentance KAFKA_BROKERS=$KAFKA_BROKERS
oc set env dc/reefercontainermaintentance KAFKA_APIKEY=$KAFKA_APIKEY
oc set env dc/reefercontainermaintentance KAFKA_CERT=/opt/app-root/src/es-cert.pem
