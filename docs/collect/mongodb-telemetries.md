# Work with Mongodb to persist telemetries

Create the service credentials and the mongodb.composed url, something starting as `mongodb://ibm_cloud_e154ff52_ed` 

Set this URL in setenv.sh the MONGO_DB_URL="mongodb://ibm_c..."

Get the certificate as pem file

```
ibmcloud cdb deployment-cacert gse-eda-mongodb > mongodbca.pem
```

Use the pymongo driver and open a connection.

```python
 URL=os.getenv('MONGO_DB_URL')
 client = MongoClient(URL,ssl=True,ssl_ca_certs='/home/mongodb.pem')
 db = client.ibmclouddb

 # insert a record
 result = db.telemetries.insert_one(telemetry)
 telemetry = db.telemetries.find_one({"_id": ObjectId(result.inserted_id)})

 # get all the records
 telemetries = db.telemetries.find()
 for t in telemetries:
```

See the rest of the code in `ml/data/ToMongo.py`.

## As a telemetry repository for the simulator

The approach is to use the same API, but get the pem file in the docker image and set the environment variables accordingly.

