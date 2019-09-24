export POSTGRESQL_USER=postgres
export POSTGRESQL_PWD=postgres
export POSTGRESQL_HOST=localhost

PGPASSWORD=$POSTGRESQL_PWD psql --host=$POSTGRESQL_HOST --port=5432 --username=$POSTGRESQL_USER  -d postgres