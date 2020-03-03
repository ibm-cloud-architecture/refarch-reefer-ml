
if [[ $# -eq 0 ]];then
  kcenv="LOCAL"
else
  kcenv=$1
fi


case "$kcenv" in
   IBMCLOUD)
        export KAFKA_BROKERS="broker-.....south.eventstreams.cloud.ibm.com:9093"
        export KAFKA_APIKEY=""
        export KAFKA_CERT=""
        export TELEMETRY_TOPIC="reefer-telemetry"
        export CONTAINER_TOPIC="containers"
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
        export MONGODB_USER="mongo"
        export MONGODB_PASSWORD="mongo"
        export cp4d_user=""
        export cp4d_pwd=""
        export PREDICTION_BASE_URL="https://zen-cpd-zen.apps.demo.ibmcloud.com"
        export PREDICTION_URL="/v4/deployments/be/predictions"
    ;;
   OCP)
        export KAFKA_BROKERS=icp-proxy.apps.green-with-envy.ocp.csplab.local:32016
        export KAFKA_APIKEY=""
        export KAFKA_CERT=""
        export TELEMETRY_TOPIC="reefer-telemetry"
        export CONTAINER_TOPIC="containers"
        export MONGO_DB_URL="mongodb://mongo:mongo@mongodb-36-centos7-reefershipmentsolution.apps.green-with-envy.ocp.csplab.local:27017/reeferdb"
        export MONGODB_USER="mongo"
        export MONGODB_PASSWORD="mongo"
        export MONGODB_DATABASE="reeferdb"
        export MONGODB_ADMIN_PASSWORD="admin"
        export cp4d_user=""
        export cp4d_pwd=""
        export PREDICTION_BASE_URL="https://zen-cpd-zen.apps.demo.ibmcloud.com"
        export PREDICTION_URL="/v4/deployments/b/predictions"
    ;;
    LOCAL)
        export KAFKA_APIKEY=""
        export KAFKA_BROKERS="kafka1:9092"
        export KAFKA_CERT=""
        export TELEMETRY_TOPIC="reefer-telemetry"
        export CONTAINER_TOPIC="containers"
        export MONGO_DB_URL="mongodb://i.../ibmclouddb?authSource=admin&replicaSet=replset"
        export MONGO_SSL_PEM="/home/simulator/mongodb.pem"
        export POSTGRES_URL="postgres://postgres:supersecret@localhost:5432/postgres"
        export POSTGRES_DBNAME="postgres"
        export POSTGRES_SSL_PEM=""
        export POSTGRES_HOST=localhost
        export POSTGRES_PORT=5432
        export POSTGRES_USER="prostgres"
        export POSTGRES_PWD="supersecret"
        export cp4d_user=""
        export cp4d_pwd=""
        export PREDICTION_BASE_URL="https://zen-cpd-zen.apps.demo.ibmcloud.com"
        export PREDICTION_URL="/v4/deployments/b/predictions"
    ;;
esac
