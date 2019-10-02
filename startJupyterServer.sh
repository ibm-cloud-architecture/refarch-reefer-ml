
if [[ $# -eq 0 ]];then
  kcenv="LOCAL"
else
  kcenv=$1
fi
source ./scripts/setenv.sh $kcenv

docker run  --rm -p 8888:8888 -v "$PWD":/home/jovyan/work -e KAFKA_BROKERS=$KAFKA_BROKERS \
     -e KAFKA_APIKEY=$KAFKA_APIKEY \
     -e KAFKA_ENV=$KAFKA_ENV  \
     -e POSTGRES_URL=$POSTGRES_URL \
     --network docker_default\
     -e POSTGRES_DBNAME=$POSTGRES_DBNAME \
     -e POSTGRES_SSL_PEM=$POSTGRES_SSL_PEM\
     ibmcase/jupyter 

