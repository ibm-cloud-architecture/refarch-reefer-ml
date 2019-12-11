
if [[ $# -eq 0 ]];then
  kcenv="LOCAL"
else
  kcenv=$1
fi


case "$kcenv" in
   IBMCLOUD)
        export KAFKA_BROKERS="broker-.....south.eventstreams.cloud.ibm.com:9093"
        export KAFKA_APIKEY=""
        export POSTGRES_URL="postgres://<user>:<pwd>@<host>:32347/ibmclouddb?sslmode=verify-full"
        export POSTGRES_DBNAME="ibmclouddb"
        export POSTGRES_SSL_PEM="./postgres.pem"
        export POSTGRES_USER=""
        export POSTGRES_PWD=""
        export POSTGRES_HOST="databases.appdomain.cloud"
        export POSTGRES_PORT=32347
        export MONGO_DB_URL="mongodb://i.../ibmclouddb?authSource=admin&replicaSet=replset"
        export MONGODB_DATABASE="ibmclouddb"
        export MONGO_SSL_PEM="/home/simulator/mongodb.pem"
    ;;
   CP)
        export KAFKA_BROKERS=icp-proxy.apps.green-with-envy.ocp.csplab.local:32016
        export KAFKA_APIKEY=""
        export MONGO_DB_URL="mongodb://mongo:mongo@mongodb-36-centos7-reefershipmentsolution.apps.green-with-envy.ocp.csplab.local:27017/reeferdb"
        export MONGODB_USER="mongo"
        export MONGODB_PASSWORD="mongo"
        export MONGODB_DATABASE="reeferdb"
        export MONGODB_ADMIN_PASSWORD="admin"
    ;;
    LOCAL)
        export KAFKA_APIKEY=""
        export KAFKA_BROKER="kafka1:9092" 
        export MONGO_DB_URL="mongodb://i.../ibmclouddb?authSource=admin&replicaSet=replset"
        export MONGO_SSL_PEM="/home/simulator/mongodb.pem"
        export POSTGRES_URL="postgres://postgres:supersecret@localhost:5432/postgres"
        export POSTGRES_DBNAME="postgres"
        export POSTGRES_SSL_PEM=""
        export POSTGRES_HOST=localhost
        export POSTGRES_PORT=5432
        export POSTGRES_USER="prostgres"
        export POSTGRES_PWD="supersecret"
    ;;
esac