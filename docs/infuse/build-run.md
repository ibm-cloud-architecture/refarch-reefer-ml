

### An alternate approach is to setup a CI/CD pipeline

We have adopted the Git Action to manage the [continuous integration](https://github.com/ibm-cloud-architecture/refarch-kc-gitops/blob/master/KContainer-CI-Strategy.md), and ArgoCD for the continuous deployment. The build process will build the following images:

* [https://hub.docker.com/repository/docker/ibmcase/kcontainer-reefer-simulator]

Helm charts are added for the simulator and the scoring agent, using `helm create` command, and then the values.yaml and deployment.yaml files were updated to set environment variables and other parameters.

## Test sending a simulation control to the POST api

The script `sendSimulControl.sh` is used for that. The usage looks like:  `sendSimulControl.sh hostname simultype (co2sensor | o2sensor | poweroff) containerID nb_of_records`

```
pwd
refarch-reefer-ml
./scripts/sendSimulControl.sh reefersimulatorroute-reefershipmentsolution.apps.green-with-envy.ocp.csplab.local co2sensor C01 2000
```

If you use no argument for this script, it will send co2sensor control to the service running on our openshift cluster on IBM Cloud.

Looking at the logs from the pod using `oc logs reefersimulator-3-jdh2v` you can see something like:

```
     "POST /order HTTP/1.1" 404 232 "-" "curl/7.54.0"
    {'containerID': 'c100', 'simulation': 'co2sensor', 'nb_of_records': 10, 'good_temperature': 4.4}
    Generating  10  Co2 metrics
```

We will see how those events are processed in the next section.



## The predictive scoring agent

Applying the same pattern as the simulation webapp, we implement a kafka consumer and producer in python that calls the serialized analytical model. The code in the `scoring\eventConsumer` folder.

Applying a TDD approach we start by a TestScoring.py class.

```python
import unittest
from domain.predictservice import PredictService

class TestScoreMetric(unittest.TestCase):
    def testCreation(self):
        serv = PredictService
        
if __name__ == '__main__':
    unittest.main()
```

Use the same python environment with docker:

```
./startPythonEnv
root@1de81b16f940:/# export PYTHONPATH=/home/scoring/eventConsumer
root@1de81b16f940:/# cd /home/scoring/eventConsumer
root@1de81b16f940:/home/scoring/eventConsumer# python tests/TestScoring.py 
```

Test fails, so let add the scoring service with a constructor, and load the serialized pickle model (which was copied from the ml folder).

```python
import pickle

class PredictService:
    def __init__(self,filename = "domain/model_logistic_regression.pkl"):
        self.model = pickle.load(open(filename,"rb"),encoding='latin1')
    
    
    def predict(self,metricEvent):
        TESTDATA = StringIO(metricEvent)
        data = pd.read_csv(TESTDATA, sep=",")
        data.columns = data.columns.to_series().apply(lambda x: x.strip())
        X = data[ X = data[FEATURES_NAMES]]
        return self.model.predict(X)
    
```

Next we need to test a predict on an event formated as a csv string. The test looks like:

```
    serv = PredictService()
    header="""Timestamp, ID, Temperature(celsius), Target_Temperature(celsius), Power, PowerConsumption, ContentType, O2, CO2, Time_Door_Open, Maintenance_Required, Defrost_Cycle"""
    event="2019-04-01 T16:29 Z,1813, 101, 4.291843460900875,4.4,0,10.273342381017777,3,4334.920958996634,4.9631508046318755,1,0,6"""
    record=header+"\n"+event
    print(serv.predict(record))
```

So the scoring works, now we need to code the scoring application that will be deployed to Openshift cluster, and which acts as a consumer of container metrics events and a producer container events. 

The Scoring Agent code of this app is [ScoringAgent.py](https://github.com/ibm-cloud-architecture/refarch-reefer-ml/blob/master/scoring/ScoringAgent.py) module. It starts a consumer to get messages from Kafka. And when a message is received, it needs to do some data extraction and transformation and then use the predictive service.

During the tests we have issue in the data quality, so it is always a good practice to add a validation function to assess if all the records are good. For production, this code needs to be enhanced for better error handling an reporting.

### Run locally

Under `scoring\eventConsumer` folder, set the environment variables for KAFKA using the commands below: (It uses event streams on IBM Cloud)

```
export KAFKA_BROKERS=broker-3.eventstreams.cloud.ibm.com:9093,broker-1.eventstreams.cloud.ibm.com:9093,broker-0.eventstreams.cloud.ibm.com:9093,broker-5.eventstreams.cloud.ibm.com:9093,broker-2.eventstreams.cloud.ibm.com:9093,broker-4.eventstreams.cloud.ibm.com:9093
export KAFKA_APIKEY="set-api-key-for-eventstreams-on-cloud"

docker run -e KAFKA_BROKERS=$KAFKA_BROKERS -e KAFKA_APIKEY=$KAFKA_APIKEY  -v $(pwd)/..:/home -ti ibmcase/python bash -c "cd /home/scoring && export PYTHONPATH=/home && python ScoringAgent.py"
```

### Scoring: Build and run on Openshift

The first time we need to add the application to the existing project, run the following command:

```
oc new-app python:latest~https://github.com/ibm-cloud-architecture/refarch-reefer-ml.git --context-dir=scoring/eventConsumer --name reeferpredictivescoring
```

This command will run a source to image, build all the needed yaml files for the kubernetes deployment and start the application in a pod. It use the `--context` flag to define what to build and run. With this capability we can use the same github repository for different sub component.

As done for simulator, the scoring service needs environment variables. We can set them using the commands

```
oc set env dc/reeferpredictivescoring KAFKA_BROKERS=$KAFKA_BROKERS
oc set env dc/reeferpredictivescoring KAFKA_APIKEY=$KAFKA_APIKEY
oc set env dc/reeferpredictivescoring KAFKA_CERT=/opt/app-root/src/es-cert.pem
```

but we have added a script for you to do so. This script needs only to be run at the first deployment. It leverage the common setenv scripts:

```
../scripts/defEnvVarInOpenShift.sh 
```

The list of running pods should show the build pods for this application:

```
 oc get pods
 reeferpredictivescoring-1-build   1/1       Running      0          24s
```

To run the build again after commit code to github:

```
oc start-build reeferpredictivescoring 

# or from local file system
oc start-build reeferpredictivescoring --from-file=.
```

To see the log:

```
 oc logs reeferpredictivescoring-2-rxr6j
```

To be able to run on Openshift, the APP_FILE environment variable has to be set to ScoringApp.py. This can be done in the `environment` file under the `.s2i ` folder.

The scoring service has no API exposed to the external world, so we do not need to create a `Route` or ingress.

See the [integration test](#integration-tests) section to see a demonstration of the solution end to end.


### Build docker images



For the scoring agent:

```
# scoring folder

```

#### Run kafka on your laptop

For development purpose, you can also run kafka, zookeeper and postgresql and the solution on your laptop. For that read [this readme](https://github.com/ibm-cloud-architecture/refarch-reefer-ml/blob/master/docker/README.md) for details.