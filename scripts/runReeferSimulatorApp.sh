if [[ $# -eq 0 ]];then
  kcenv="LOCAL"
else
  kcenv=$1
fi
source ./scripts/setenv.sh $kcenv

docker run -e KAFKA_BROKERS=$KAFKA_BROKERS \
     -e KAFKA_APIKEY=$KAFKA_APIKEY \
     -e KAFKA_CERT=$KAFKA_CERT \
     -e MONGO_DB_URL=$MONGO_DB_URL \
     -e MONGO_DATABASE=$MONGODB_DATABASE \
     -e MONGO_SSL_PEM=$MONGO_SSL_PEM\
     -p 8080:8080 \
     ibmcase/kcontainer-reefer-simulator

