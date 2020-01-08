# PostgreSQL on IBM Cloud

We are using Postgresql as a data source to persist Product and Container information. The Produts table is used in the predictive model construction. So we need to provision a Postgresql service in IBM Cloud. Use the [product documentation](https://cloud.ibm.com/docs/services/databases-for-postgresql) to provision your own service. 

Here is a figure of the databases services in IBM Cloud as of December 2019.

![](images/ibm-cloud-dbs.png)

Using the default configuration the service is created in a minutes. Once done, we need to define the service credentials for the host, user, password and the certificate to be used by client appliations.

![](images/postgres-credential.png)

Something like that:

```
"host=bd2d0216-0b7d-4575-8c0b-d2e934843e41.6131b73286f34215871dfad7254b4f7d.databases.appdomain.cloud port=31384 
dbname=ibmclouddb 
user=ibm_cloud_c958... 
"PGPASSWORD": "2d1c526.....3"
```

From these informations we need to define  the POSTGRES environment variables in the `scripts/setenv.sh` file. (if not done before rename the `scripts/setenv-tmpl.sh` to `scripts/setenv.sh`)

```
POSTGRES_URL,  POSTGRES_DBNAME,
```

You also need to get the SSL certificate as a `postgres.pem` file, using the following ibmcloud CLI commands:
        
```shell
ibmcloud login
ibmcloud cdb deployment-cacert <database deployment name>
```

Then in `setenv.sh` set `POSTGRES_SSL_PEM` variable to the path where to find this file (`export POSTGRES_SSL_PEM="./certs/postgres.pem"`). 

## Connect with psql

To validate the access, we use a public postgres docker image to run `psql` using the defined environment variables.  We have a script to start it:

```shell
$ cd scripts
$ ./startPsql.sh IBMCLOUD
root@452074de376a:/# PGPASSWORD=$POSTGRES_PWD psql --host=$HOST --port=$PORT --username=$POSTGRES_USER --dbname=$POSTGRES_DB
ibmclouddb => 
```

### List relations...

```
ibmclouddb => \d
```

## Next...

You can use our tool to add some product definitions, for that see [this note...](../collect/products-postgres.md)