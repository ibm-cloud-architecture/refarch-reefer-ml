
#!/bin/bash
if [[ $# -ne 1 ]];then
 echo "Usage startPsql.sh [LOCAL  | IBMCLOUD ]"
 exit 1
fi

source ../../../scripts/setenv.sh $1

docker run -ti -v $(pwd):/home \
  -e POSTGRES_USER=$POSTGRES_USER \
  -e POSTGRES_PWD=$POSTGRES_PWD \
  -e POSTGRES_DB=$POSTGRES_DBNAME \
  -e HOST=$POSTGRES_HOST \
  -e PORT=$POSTGRES_PORT postgres bash 
  
  # -c "PGPASSWORD=$POSTGRES_PWD psql --host=$HOST --port=$PORT --username=$POSTGRES_USER --dbname=$POSTGRES_DB"
