
#!/bin/bash
if [[ $# -ne 1 ]];then
 echo "Usage startPsql.sh [LOCAL  | IBMCLOUD ]"
 exit 1
fi

source ./scripts/setenv.sh $1

PGPASSWORD=$POSTGRES_PWD psql --host=$POSTGRES_HOST --port=$POSTGRES_PORT \
--username=$POSTGRES_USER  -d $POSTGRES_DBNAME
