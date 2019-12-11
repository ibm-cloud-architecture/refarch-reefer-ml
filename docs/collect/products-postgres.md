# Define the products data into postgresql

We are using a Postgresql instance on IBM Cloud. So once you create your own instance get the credential for the host, user, password and the certificate.

```
"host=bd2d0216-0b7d-4575-8c0b-d2e934843e41.6131b73286f34215871dfad7254b4f7d.databases.appdomain.cloud port=31384 
dbname=ibmclouddb 
user=ibm_cloud_c958... 
"PGPASSWORD": "2d1c526.....3"
```

First be sure to set at least the following environment variables in the `setenv.sh` file

```
POSTGRES_URL,  POSTGRES_DBNAME,
```

If you use POSTGRESQL on IBM Cloud or any deployment using SSL, you need to get the SSL certificate as `postgres.pem` file, or set `POSTGRES_SSL_PEM` variable to the path where to find this file.

## Populate the products data with the Simulator repository

The simulator code includes the [infrastructure/ProductRepository.py]() that can create tables and add some product definitions inside the table.
The following command using docker and python interpreter can create the database:

```
./scripts/createPGTables.sh IBMCLOUD
```

And alternate techniques is to use [psql](https://www.postgresql.org/docs/9.3/app-psql.html)

## Connect with psql

We use a docker image to run psql:

```shell
# under the data_schema/rdbms/postgresql folder
$ ./startPsql.sh IBMCLOUD
$ PGPASSWORD=$POSTGRES_PWD psql --host=$HOST --port=$PORT --username=$POSTGRES_USER --dbname=$POSTGRES_DB
ibmclouddb => 
```

## List relations...

```
ibmclouddb => \d
```

Then create table if not done before
```
ibmclouddb => CREATE TABLE products (
    product_id varchar(64) NOT NULL PRIMARY KEY,
    description varchar(100),
    target_temperature REAL,
    target_humidity_level REAL
);
```

Populate the data:

```
ibmclouddb => INSERT INTO products(product_id,description,target_temperature,target_humidity_level) VALUES
('P01','Carrots',4,0.4),
('P02','Banana',6,0.6),
('P03','Salad',4,0.4),
('P04','Avocado',6,0.4),
('P05','Tomato',4,0.4);
```

List the products
```
SELECT * FROM products;
```

You should see:
```
 product_id | description | target_temperature | target_humidity_level | content_type 
------------+-------------+--------------------+-----------------------+--------------
 P01        | Carrots     |                  4 |                   0.4 |            1
 P02        | Banana      |                  6 |                   0.6 |            2
 P03        | Salad       |                  4 |                   0.4 |            1
 P04        | Avocado     |                  6 |                   0.4 |            2
 P05        | Tomato      |                  6 |                   0.3 |            6
```

Quit 
```
ibmclouddb => \q
```