# Define the products data into postgresql

The Simulator references product data stored in a Postgresql database.  There are multiple ways to populate this database depending on your level of experience with Postgresql, database services, and your local development environment.

We have provided the following documented methods for populating the Product database:
1. [Kubernetes Job running remote cluster](#kubernetes-job-running-remote-cluster) _(RECOMMENDED)_
2. [Docker image running on local machine](#docker-image-running-on-local-machine)
3. [Postgresql CLI (psql) running on local machine](#postgresql-cli-psql-running-on-local-machine)

## Kubernetes Job running remote cluster

In an effort to keep development systems as clean as possible and speed up deployment of various scenarios, our deployment tasks have been encapsulated in [Kubernetes Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/). These are runnable on any Kubernetes platform, including OpenShift.

1. Following the configuration prerequisistes defined in the [Backing Services](https://ibm-cloud-architecture.github.io/refarch-kc/deployments/backing-services/#using-postgresql-hosted-on-ibm-cloud) documentation for using [Databases for PostgreSQL](https://cloud.ibm.com/catalog/services/databases-for-postgresql) on IBM Cloud, you should already have the following Kubernetes Secrets defined in your target namespace:
   1. `postgresql-url` _(in the format of `jdbc:postgresql://<hostname>:<port>/<database-name>?sslmode=...`)_
   2. `postgresql-user`
   3. `postgresql-pwd`
   4. `postgresql-ca-pem`
2. Create the `create-postgres-tables` Job from the root of the `refarch-reefer-ml` repository:
```shell
kubectl apply -f scripts/createPGtables.yaml
```
3. You can tail the created pod's output to see the progress of the database initialization:
```shell
kubectl logs -f --selector=job-name=create-postgres-tables
```

## Docker image running on local machine

The simulator code includes the [infrastructure/ProductRepository.py](https://github.com/ibm-cloud-architecture/refarch-reefer-ml/blob/master/simulator/infrastructure/ProductRepository.py) that creates tables and adds some product definitions inside the table.

1. Uncomment line 101 from `/simulator/infrastructure/ProductRepository.py`:
```python
    # repo.populateProductsReferenceData()
```
2. The following command is using our python environment docker image and the python code:
```shell
./scripts/createPGTables.sh IBMCLOUD
```

## Postgresql CLI (psql) running on local machine

An alternate techniques is to use [psql](https://www.postgresql.org/docs/9.3/app-psql.html) as described in this section. Previous experience with PSQL is recommended.

1. We use a docker image to run psql:

```shell
$ cd scripts
$ ./startPsql.sh IBMCLOUD
$ PGPASSWORD=$POSTGRES_PWD psql --host=$HOST --port=$PORT --username=$POSTGRES_USER --dbname=$POSTGRES_DB
ibmclouddb =>
```

2. List relations...

```psql
ibmclouddb => \d
```

3. Then create table if not done before:

```psql
ibmclouddb => CREATE TABLE products (
    product_id varchar(64) NOT NULL PRIMARY KEY,
    description varchar(100),
    target_temperature REAL,
    target_humidity_level REAL
);
```

4. Populate the data:

```psql
ibmclouddb => INSERT INTO products(product_id,description,target_temperature,target_humidity_level) VALUES
('P01','Carrots',4,0.4),
('P02','Banana',6,0.6),
('P03','Salad',4,0.4),
('P04','Avocado',6,0.4),
('P05','Tomato',4,0.4);
```

5. List the products

```psql
SELECT * FROM products;
```

You should see:
```psql
 product_id | description | target_temperature | target_humidity_level | content_type
------------+-------------+--------------------+-----------------------+--------------
 P01        | Carrots     |                  4 |                   0.4 |            1
 P02        | Banana      |                  6 |                   0.6 |            2
 P03        | Salad       |                  4 |                   0.4 |            1
 P04        | Avocado     |                  6 |                   0.4 |            2
 P05        | Tomato      |                  6 |                   0.3 |            6
```

6. Exit the PSQL environment
```psql
ibmclouddb => \q
```
