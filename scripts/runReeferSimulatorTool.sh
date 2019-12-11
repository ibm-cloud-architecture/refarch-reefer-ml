if [[ $# -eq 0 ]];then
  kcenv="LOCAL"
else
  kcenv=$1
fi
source ./scripts/setenv.sh $kcenv
shift

docker run -v $(pwd):/home -e KAFKA_BROKERS=$KAFKA_BROKERS \
     -e KAFKA_APIKEY=$KAFKA_APIKEY \
     -e MONGO_DB_URL=$MONGO_DB_URL \
     -e MONGO_DATABASE=$MONGODB_DATABASE \
     -e MONGO_SSL_PEM=$MONGO_SSL_PEM\
     -ti ibmcase/python bash
     
# "python simulator/reefer_simulator_tool.py $@"

