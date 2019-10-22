
if [[ $# -eq 0 ]];then
  kcenv="LOCAL"
else
  kcenv=$1
fi
source ./scripts/setenv.sh $kcenv

if [[ -z "$IPADDR" ]]
then
    export IPADDR=$(ifconfig en0 |grep "inet " | awk '{ print $2}')
fi


if [[ $kcenv == "LOCAL" ]]
then
  docker run -e DISPLAY=$IPADDR:0 -v $(pwd):/home -e KAFKA_BROKERS=$KAFKA_BROKERS \
     -e KAFKA_APIKEY=$KAFKA_APIKEY \
     -e POSTGRES_URL=$POSTGRES_URL \
     --network docker_default\
     -e POSTGRES_DBNAME=$POSTGRES_DBNAME \
     -e POSTGRES_SSL_PEM=$POSTGRES_SSL_PEM\
      -ti ibmcase/python bash
else
  docker run  -e DISPLAY=$IPADDR:0 -v $(pwd):/home -e KAFKA_BROKERS=$KAFKA_BROKERS \
     -e KAFKA_APIKEY=$KAFKA_APIKEY \
     -e POSTGRES_URL=$POSTGRES_URL \
     --network host \
     -e POSTGRES_DBNAME=$POSTGRES_DBNAME \
     -e POSTGRES_SSL_PEM=$POSTGRES_SSL_PEM\
      -ti ibmcase/python bash
fi
