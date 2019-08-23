# Reefer Predictive Maintenance Solution

This project is to demonstrate how to perform real time scoring on Reefer container metrics. The runtime environment in production will look like:

![](images/RT-analytics.png)

The Reefer container is a IoT device, which emits container metrics every 15 minutes via the MQTT protocol. The first component receiving those messages is Apache Nifi to transform the metrics message to a kafka event. Kafka is used as the event backbone and event sourcing so microservices, deployed on openshift, can consume and publish messages.

For persistence reason, we may leverage big data type of storage like Cassandra to persist the container metrics over a longer time period. This datasource is used by the Data Scientists to do its data preparation and build training and test sets and build model.

Data scientists can run Jupyter lab on OpenShift and build a model to be deployed as python microservice, consumer of kafka Reefer metrics events. The action will be to change the state of the Reefer entity via an events to the `containers` topic. 

While for the minimum viable demonstration the components looks like in the figure below:

![](images/mvp-runtime.png)

1. A web app, deployed on Openshift, is running a simulator to simulate the generation of Reefer container metrics while the container is at sea or during end to end transportation. The app exposes a simple POST operation with a control object to control the simulation. Here is an example of such control.json

    ```json
    { 'containerID': 'c100',
    'simulation': 'co2sensor',
    'nb_of_records': 1000,
    'good_temperature': 4.4
    }
    ```

1. A curl script will do the post of this json object
1. The metrics events are sent to the `containerMetrics` topic in Kafka
1. The predictive scoring is a consumer of such events, read one event at a time and call the model internally, then sends a new event when maintenance is required.
1. The maintenance requirement is an event in the `containers` topic.
1. The last element is to trace the container maintenance event, in real application, this component should trigger a business process to get human performing the maintenance.

## Pre-requisites

Start by cloning this project using the command:

```
git clone https://github.com/jbcodeforce/refarch-reefer-ml
```


### Building the python environment as docker image

To avoid impacting our environment, we use a dockerfile to get the basic of python 3.7.x and other needed modules like kafka, http requests, pytest... So to build your python image with all the needed libraries, use the following commands:

```
cd docker
docker build -f docker-python-tools -t ibmcase/python .
```

### Be sure to have Event Stream or kafka running

Create the Event Stream service using the [IBM Cloud catalog](https://cloud.ibm.com/catalog/services/event-streams)

The following diagram illustrates the topics configured in IBM Cloud Event Stream service:

![](images/es-topics.png)

In the service credentials creates new credentials to get the Kafka broker list, the admin URL and the api_key needed to authenticate the consumers or producers.

## Machine Learning Work

To review the problem of predictive maintenance read [this article.](predictive-maintenance.md)

### Generate data with the Reefer simulator

Well we do not have real Reefer data. But we may be able to simulate them. As this is not production work, we should be able to get the end to end story still working from a solution point of view.

The historical data need to represent failure, and represent the characteristics of a Reefer container. We can imagine it includes a lot of sensors to get interesting correlated or independant features.

We have implemented a simulator to create those metrics to be used to build the model inside Jupiter notebook and with sklearn or tensorflow library. 

#### Start python env

```
 ./startPythonEnv 

root@03721594782f: cd /home/simulator
```

From this shell, first specify where python should find the new modules, by setting the environment variable PYTHONPATH:

```
root@03721594782f:/# export PYTHONPATH=/home
```

#### Generate power off metrics

When the reefer containers lose power at some time, the temperature within the container starts raising.

The simulator accepts different arguments: 

```
usage reefer_simulator --stype [poweroff | co2sensor | atsea]
	 --cid <container ID>
	 --records <the number of records to generate>
	 --temp <expected temperature for the goods>
	 --file <the filename to create (without .csv)>
	 --append [yes | no]  (reuse the data file)
```
 
```
    root@03721594782f: python reefer_simulator_tool.py --stype poweroff --cid 101 --records 1000 --temp 4 --file ../ml/data/metrics.csv --append yes

    Generating  1000  poweroff metrics

    Timestamp   ID  Temperature(celsius) Target_Temperature(celsius)      Power  PowerConsumption ContentType  O2 CO2  Time_Door_Open Maintenance_Required Defrost_Cycle
    1.000000  2019-06-30 T15:43 Z  101              3.416766                           4  17.698034          6.662044           1  11   1        8.735273                    0             6
    1.001001  2019-06-30 T15:43 Z  101              4.973630                           4   3.701072          8.457314           1  13   3        5.699655                    0             6
    1.002002  2019-06-30 T15:43 Z  101              1.299275                           4   7.629094 
```     

#### Generate Co2 sensor malfunction in same file

In the same way as above the simulator can generate data for Co2 sensor malfunction using the command:

```
python reefer_simulator_tool.py --stype co2sensor --cid 101 --records 1000 --temp 4 --file ../ml/data/metrics.csv --append yes
```

!!! note
        The simulator is integrated in the event producer to send real time events to kafka, as if the Reefer container was loaded with fresh goods and is travelling oversea. A consumer code can call the predictive model to assess if maintenance is required and post new event on a `containers` topic.

### Create the model

Now we will use a local version of **Jupyter** notebook to load the logistic regression nodebook in the `ml` folder. 

1. Start a jupyter server using a docker image:

    ```
    cd ml
    docker run --rm -p 10000:8888 -v "$PWD":/home/jovyan/work jupyter/datascience-notebook
    ```

1. Then open a web browser to `http://localhost:10000` and then open the `model_logistic_regression.ipynb` and run it step by step. The notebook includes comments to explain how the model is done. We use logistic regression to build a binary classification (maintenance required or not), as the data are simulated, and the focus is not in the model building, but more on the end to end process.
The notebook persists the trained model as a pickle file so it can be loaded by a python module or another model.

    For more information on using the Jupyter notebook, here is a [product documentation](https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html).

1. Use the model in another notebook: We can use a second notebook to assess some one record test using the pickle serialized model. The notebook is named `predictMaintenance.ipynb`

## The Simulator as webapp

This is a simple python Flask web app exposing a REST POST end point and producing Reefer metrics event to kafka. 
The POST operation in on the /control url. The control object, to generate 1000 events with the co2sensor simulation looks like:

```json
    { 'containerID': 'c100',
    'simulation': 'co2sensor',
    'nb_of_records': 1000,
    'good_temperature': 4.4
    }
```

### Run it locally

To build the simulator using the [s2i CLI](https://github.com/openshift/source-to-image):

```
s2i build --copy .  centos/python-36-centos7 ibmcase/reefersimulator
```

Then to run it locally, use the local script `./runReeferSimulator.sh ` or after setting the environment variables for kafka launch the docker container like:

```
docker run -p 8080:8080 -e KAFKA_ENV=$KAFKA_ENV -e KAFKA_BROKERS=$KAFKA_BROKERS -e KAFKA_APIKEY=$KAFKA_APIKEY ibmcase/reefersimulator
```

### Build and run on OpentShift

To deploy the code to an openshift cluster do the following:

1. Login to the openshift cluster. 

    ```
    oc login -u apikey -p <apikey> --server=https://...
    ```

1. Create a project if not done already:

    ```
    oc  new-project order-producer-python --description="A kafka producer with python"
    ```

1. Create an app from the source code, and use source to image build process to deploy the app:

    ```
    oc new-app python:latest~https://github.com/jbcodeforce/refarch-reefer-ml/simulator -name order-producer-python
    ```

    Then to track the deployment progress:
    ```
    oc logs -f bc/order-producer-python
    ```
    The dependencies are loaded, the build is scheduled and executed, the image is uploaded to the registry, and started.

1. To display information about the build configuration for the application:

    ```
    oc describe bc/order-producer-python
    ```






