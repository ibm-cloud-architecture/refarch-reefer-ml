# IBM Cloud Pak Approach

The goal of this approach is to use the following cloud Pak to develop and deploy the solution. The following diagram illustrates the features or components used in each cloud paks to support the implementation.

![](images/cp-approach.png)

The grey components are part of the solution implementation. 

## Preparing the different environments

The numbered figure below, illustrates the step by step environment setup:

![](images/cp-approach-num.png)

### 1- PostgreSQL Service

The products database is defined in PostgreSQL service within IBM Cloud public. See [this note](collect/products-postgres.md) for details on how to use this service and the python code in the simulator folder or the psql tool to create the product database. 

### 2- MongoDB Service

The long term persistence for the telemetry metrics we are using mongodb on IBM Cloud. This [separate note](collect/generate-telemetry.md) goes into details on how we prepare the data and upload them to mongo.

### 3- Openshift 4.2 Cluster for CP4I and CP4App

To install Openshift 4.2 cluster we recommend following Red Hat tutorials and [our cookbook]().

### 4- Deploy event streams and defines topics

We are presenting a quick overview of deploying IBM Event Streams from Cloud pak for Integration and how to configure the needed Kafka topics in [this note](collect/event-streams.md).


### 5- Deploy Cloud Pak for Application


See also the reference architecture [article for application modernization](https://www.ibm.com/cloud/garage/architectures/application-modernization).

### 6- Reefer simulator as Appsody Python

We are presenting how we used the Appsody python template as a based to implement the Reefer simulator combined with other python development best practices, in [this note](infuse/simul-app.md).

### 7- Scoring microservice as Java Microprofile app

### 8- Data Virtualization 

### 9- Anomaly detection notebook

### 10- Anomaly detection service

### 11- Cloud Pak for Automation

### 12- Reefer Maintenance business process

