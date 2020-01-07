# Build the solution - Workshop

## Pre-requisites to build and run this solution

Start by cloning this project using the command:

```
git clone https://github.com/ibm-cloud-architecture/refarch-reefer-ml
```

### Repository structure

The solution to implement includes the following components:

![Components](./images/mvp-runtime.png)

* The Reefer simulator (1) to send telemetry events or to create such data elements as CSV file. The code is under `simulator` folder.
* The curl call (2) is done in a script: `scripts/sendSimulControl.sh`
* The scoring agent (4) is in the `scoring` folder or if you are using IBM Cloud Pak solution it is a Java Microprofile applicating in the `scoring-mp` folder.
* The Reefer container service (6) is in a separate project, but we have defined a docker image, [published in docker hub](https://hub.docker.com/repository/docker/ibmcase/kcontainer-spring-container-ms) so we propose to deploy it on Openshift in [this section](#deploy-reefer-container)
* The business process definition (7) is in the twx file under the `bpm` folder.

### Building a python development environment as docker image

To avoid impacting our laptop environment (specially macbook which use python), we use a dockerfile to get the basic of python 3.7.x and the python modules like kafka, http requests, pandas, sklearn, pytest... we need to develop and test the different python code of this solution. To build your python image with all the needed libraries, use the following commands:

```
cd docker
docker build -f docker-python-tools -t ibmcase/python .
```

To use this python environment you can use the script: `startPythonEnv`. 

When running with Event Stream and Postgres DB on the cloud use IBMCLOUD argument, if you use and on-premise Openshif cluster use the OCP argument.

```
# refarch-reefer-ml project folder
./startPythonEnv.sh IBMCLOUD
```


### Set environment variables

As part of the [12 factors practice](https://12factor.net/), we externalize the end points configuration in environment variables. We are providing a script template (`scripts/setenv-tmp.sh`) to set those variables for your local development. Rename this file as `setenv.sh`. This file is git ignored, to do not share keys and passwords in public domain.

The variables help the different code in the solution to access the Event Stream broker cluster and the Postgresql service running on IBM Cloud.


## Deploy Reefer Container

### Deploy on Openshift

We use image deployment with the following command:

```shell
oc new-app ibmcase/kcontainer-spring-container-ms
oc expose svc/kcontainer-spring-container-ms
```