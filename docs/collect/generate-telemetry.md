# Generate telemetry data

We are using the simulator to generate data. In the industry, when developing new manufactured product, the engineers do not have a lot of data so they also use a mix of real sensors with simulators to create fake but realistic data to develop and test their models.

The historical data need to represent failure, and represent the characteristics of a Reefer container. We have define some sensors to get interesting correlated or independant features.

As of now our telemetry event structure can be seen in this [avro schema](https://github.com/ibm-cloud-architecture/refarch-reefer-ml/tree/master/data_schema/reefer_telemetry_value.avsc).


For the machine learning environment we can use csv file as input data or mongodb database or kafka topic.  The environment looks like in the figure below:

![](images/data-collect.png)

The simulator can run as a standalone tool to create training and test data to be saved in a remote mongodb database or can be used to save to csv file. We use mongodb as a service on IBM cloud. 

![](images/ibm-cloud-dbs.png)


We also use reference data like products and shipping container inventory in Postgresql on IBM Cloud too. The service has credential with URL and SSL certificate.

![](images/postgres-credential.png)

## Create reference data in postgresql

See [this separate note](../products-postgres) for detail.

## Start python environment

Use IBMCLOUD if you use mongodb, postgresql and kafka on cloud, or LOCAL for kafka and postgresql running via docker compose.

```
 ./startPythonEnv IBMCLOUD or LOCAL

root@03721594782f: cd /home
```

In the Dockerfile we set the first PYTHONPATH to `/home` to specify where python should find the application specifics modules. 


## Generate data as csv file

### Generate power off metrics

When a reefer container loses power, restart and reloose it, it may become an issue. This is the goal of this simulation.

The simulator accepts different arguments as specified below 

```
usage reefer_simulator-tool 
     --stype [poweroff | co2sensor | o2sensor | normal]
	  --cid [C01 | C02 | C03 | C04 | C05]
	 --product_id [ P01 | P02 | P03 | P04 | P05 ]
	 --records <the number of records to generate>
	 --file <the filename to create>
	 --append
	 --db
```

* The `cid` is for the container id. As the simulator is taking some data from internal datasource you can use only one of those values: `[C01 | C02 | C03 | C04 | C05]`
* `product_id` is also one of the value `[ P01 | P02 | P03 | P04 | P05]`, as the simulator will derive the target temperature and humidity level from its internal datasource:
    ('P01','Carrots',1,4,0.4),
    ('P02','Banana',2,6,0.6),
    ('P03','Salad',1,4,0.4),
    ('P04','Avocado',2,6,0.4),
    ('P05','Tomato',1,6,0.4);
* `--db` is when you want to save the telemetry into mongodb DB. In this case be sure to have set the credentials and URL in the `scripts/setenv.sh` script (see the `scripts/setenv-tmp.sh` template file)
* `--file` is to specify a csv file to write the data
* `--append` is used to append the output of this run to an existing file: It permits to accumulate different simulation in the same dataset.

* (Re)create a new file. It is an important step to get the header as first row.

```shell
python simulator/reefer_simulator_tool.py --stype poweroff --cid C01 --records 1000 --product_id P02 --file telemetries.csv 
```

* append to existing file

```shell
python simulator/reefer_simulator_tool.py --cid C03 --product_id P03 --records 1000 --file telemetries.csv --stype poweroff --append
```

The results looks like:

```
    Generating  1000  poweroff metrics

    Timestamp   ID  Temperature(celsius) Target_Temperature(celsius)      Power  PowerConsumption ContentType  O2 CO2  Time_Door_Open Maintenance_Required Defrost_Cycle
    1.000000  2019-06-30 T15:43 Z  101              3.416766                           4  17.698034          6.662044           1  11   1        8.735273                    0             6
    1.001001  2019-06-30 T15:43 Z  101              4.973630                           4   3.701072          8.457314           1  13   3        5.699655                    0             6
    1.002002  2019-06-30 T15:43 Z  101              1.299275                           4   7.629094 
```     

From the two previous commands you should have 2001 rows (one for the header which will be used in the model creation):
```
wc -l telemetries.csv 
2001 telemetries.csv
```

### Generate Co2 sensor malfunction in same file

In the same way as above the simulator can generate data for Co2 sensor malfunction using the command:

```
python simulator/reefer_simulator_tool.py --cid C03 --product_id P02 --records 1000 --file basedata --stype co2sensor --append
```


!!! note
        The simulator is integrated in the event producer to send real time events to kafka, as if the Reefer container was loaded with fresh goods and is travelling oversea. A consumer code can call the predictive model to assess if maintenance is required and post new event on a `containers` topic (this consumer code is in the `scoring/eventConsumer` folder).

### Generate O2 sensor malfunction in same file

```
python simulator/reefer_simulator_tool.py --cid C03 --product_id P02 --records 1000 --file basedata --stype o2sensor --append
```

## Saving to Mongodb

The same tool can be used to save to a [mongodb](https://www.mongodb.com/) database. The document saved in mongo will not be a flat record as produced by the simulator when it creates records to Kafka, but the Json document matches the following format, where sensors are in their own object:

```json
{ "timestamp": "2019-09-04 T15:31 Z",
  "containerID": "C100",
  "product_id": "P02",
  "content_type": 2,
  "sensors": {
   "temperature": 5.49647,
   "oxygen_level" : 20.4543,
   "nitrogen_level" : 79.4046,
   "carbon_dioxide_level" : 4.42579,
   "humidity_level" : 60.3148,
   "fan_1": "True",
   "fan_2" : "True",
   "fan_3" : "True",
   "ambiant_temperature": 19.8447
  },
  "target_temperature": 6.0,
   "kilowatts": 3.44686,
   "latitude": "37.8226902168957,",
   "longitude": "-122.3248956640928",
   "time_door_open" : 0,
   "defrost_cycle": 6
}
```

First be sure to set at least the following environment variables in the `setenv.sh` file

```
MONGO_DB_URL, MONGO_SSL_PEM
```

If not done before or to ensure the mongo connection works fine, run the ReeferRepository.py tool to create the telemetries collection using the following command:

```
./startPythonEnv.sh IBMCLOUD
> python simulator/infrastructure/ReeferRepository.py
```

### Generate records in mongodb using SimulationTool

Once done run the simulator with the --db argument like below:

```
python simulator/reefer_simulator_tool.py --cid C03 --product_id P02 --records 1000  --stype poweroff --db

python simulator/reefer_simulator_tool.py --cid C03 --product_id P02 --records 1000  --stype co2sensor --db

python simulator/reefer_simulator_tool.py --cid C03 --product_id P02 --records 1000  --stype o2sensor --db
```

### Verify data with mongo CLI

To verify the data loaded into the database we use [mongo](https://docs.mongodb.com/manual/installation/) CLI with the following command:

```shell
# to connect
mongo -u $USERNAME -p $PASSWORD --tls --tlsCAFile mongodb.pem --authenticationDatabase admin --host replset/1a2ce8ca-<>.bn<>c0.databases.appdomain.cloud:30796 --tlsAllowInvalidCertificates
```

*The full host name is masked*. 

The USERNAME and PASSWORD are environment variables you set from the IBM Cloud service credentials. Something like:

```
{
  "connection": {
    "cli": {
      "arguments": [
        [
          "-u",
          "ibm_cloud_<>_48b1_b899",
          "-p",
          "3359192a<>e5fbdf51fd573676e58aff4f9e223",
```

The `mongodb.pem` is the certificate in text save in a file. To get this certificate you can use the following command:

```
ibmcloud cdb deployment-cacert gse-eda-mongodb > mongodb.pem
```

or by using the IBM Cloud mongodb service user interface (Manage menu):

![](images/tls-certificat.png)

Once connected use the ibmclouddb database with mongo CLI:

```
MongoDB server version: 4.2.0
replset:PRIMARY> use ibmclouddb
replset:PRIMARY> db.getCollection("telemetries").find()
```

### Delete records in database

In mongo CLI do:

```
db.telemetries.deleteMany({})
```


Next step is to build the model... 

