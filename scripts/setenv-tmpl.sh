
if [[ $# -eq 0 ]];then
  kcenv="LOCAL"
else
  kcenv=$1
fi


case "$kcenv" in
   IBMCLOUD)
        export KAFKA_BROKERS="broker-.....south.eventstreams.cloud.ibm.com:9093"
        export KAFKA_APIKEY=""
        export KAFKA_ENV="IBMCLOUD"
        export POSTGRES_URL="postgres://<user>:<pwd>@<host>:32347/ibmclouddb?sslmode=verify-full"
        export POSTGRES_DBNAME="ibmclouddb"
        export POSTGRES_SSL_PEM="./cert.pem"
        export POSTGRES_USER=""
        export POSTGRES_PWD=""
        export POSTGRES_HOST="databases.appdomain.cloud"
        export POSTGRES_PORT=32347
    ;;
   ICP)
        export KAFKA_BROKERS=icp-proxy.apps.green-with-envy.ocp.csplab.local:32016
        export KAFKA_APIKEY=""
    ;;
    LOCAL)
        export KAFKA_ENV="LOCAL"
        export KAFKA_APIKEY=""
        export KAFKA_BROKER="kafka1:9092" 
        export POSTGRES_URL="postgres://postgres:supersecret@localhost:5432/postgres"
        export POSTGRES_DBNAME="postgres"
        export POSTGRES_SSL_PEM=""
        export POSTGRES_HOST=localhost
        export POSTGRES_PORT=5432
        export POSTGRES_USER="prostgres"
        export POSTGRES_PWD="supersecret"
    ;;
esac