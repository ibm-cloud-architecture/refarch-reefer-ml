# Work with Mongodb to persist telemetries

MongoDB is a popular document-based database that allows developers to quickly build projects without worrying about schema. Mongo components include: 

* mongod - the core process that runs the actual database 
* mongos - controls routing to the databases in case of sharding
* config servers (CSRS) - stores the metadata in a sharded environment. 

We propose to persist telemetry for a long time period. For example we can configure Kafka topic to persist telemetries over a period of 20 days, but have another component to continuously move events as JSON documents inside mongodb or Cassandra.

So here we present how to use MongoDB on IBM Cloud to support long term persistence.

![](images/ibm-cloud-dbs.png)


## With mongodb on IBM Cloud 

Create the mongoDN service on IBM cloud using default configuration and add a service credentials to get the mongodb.composed url: (something starting as `mongodb://ibm_cloud_e154ff52_ed`) 

Set this URL in `scripts/setenv.sh` the `export MONGO_DB_URL="mongodb://ibm_c..."`

Get the TLS certificate as pem file:

```
ibmcloud cdb deployment-cacert gse-eda-mongodb > mongodbca.pem
```

## Use our docker image for python environment

Use the python pymongo driver (pip install pymongo) and open a connection with a code like below:

```python
 URL=os.getenv('MONGO_DB_URL')
 client = MongoClient(URL,ssl=True,ssl_ca_certs='/home/mongodb.pem')
 db = client['ibmclouddb']

 # insert a record
 result = db.telemetries.insert_one(telemetry)
 telemetry = db.telemetries.find_one({"_id": ObjectId(result.inserted_id)})

 # get all the records
 telemetries = db.telemetries.find()
 for t in telemetries:
```

See the rest of the `ml/data/ToMongo.py` for the code loading from CSV file, or the `simulator/infrastructure/ReeferRepository.py` for the one generating metrics and uploading them directly to mongo.

### Add data from csv file

Using the ToMongo.py script we can load the data in the telemetries.csv file. In a Terminal window uses the following commmand:

```
./startPythonEnv.sh IBMCLOUD

cd ml/data

python ToMongo.py
```

### As a telemetry repository for the simulator

The approach is to use the same APIs, but get the pem file in the docker image and set the environment variables accordingly.
The [ReeferRepository.py]() implements the mongodb operations to save telemetry.

## On Openshift 3.11 on premise

We use the following image: `centos/mongodb-36-centos7`. So to install it, we use the following command:

```
oc new-app -e \
    MONGODB_USER=mongo,MONGODB_PASSWORD=<password>,MONGODB_DATABASE=reeferdb,MONGODB_ADMIN_PASSWORD=<admin_password> \
    centos/mongodb-36-centos7
```

Connect to the pod and then use the mongo CLI

```shell
$ oc get pods
NAME                                         READY     STATUS             RESTARTS   AGE
mongodb-36-centos7-1-wcn7h                   1/1       Running            0          4d

$ oc rsh mongodb-36-centos7-1-wcn7h 
bash-4.2$ mongo -u $MONGODB_USER -p $MONGODB_PASSWORD $MONGODB_DATABASE
MongoDB shell version: 2.4.9
connecting to: reeferdb
> show collections
```

To remove the db on openshift: `oc delete dc`
