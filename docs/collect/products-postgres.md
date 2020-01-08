# Define the products data into postgresql

## Populate the products data with the Simulator repository

The simulator code includes the [infrastructure/ProductRepository.py](https://github.com/ibm-cloud-architecture/refarch-reefer-ml/blob/master/simulator/infrastructure/ProductRepository.py) that creates tables and adds some product definitions inside the table.

The following command is using our python environment docker image and the python code:

```
./scripts/createPGTables.sh IBMCLOUD
```

And alternate techniques is to use [psql](https://www.postgresql.org/docs/9.3/app-psql.html) as described below.

## Connect with psql

We use a docker image to run psql:

```shell
$ cd scripts
$ ./startPsql.sh IBMCLOUD
$ PGPASSWORD=$POSTGRES_PWD psql --host=$HOST --port=$PORT --username=$POSTGRES_USER --dbname=$POSTGRES_DB
ibmclouddb => 
```

### List relations...

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



