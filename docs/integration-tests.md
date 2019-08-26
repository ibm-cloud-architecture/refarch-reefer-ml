# Integration tests to proof the solution

Recall that the architecture of the deployed components look like in the figure below: 

![](images/mvp-runtime.png)

So the first component to start is the container consumer which consumes events from the kafka `containers` topic. This topic is where the microservices will post messages about a Reefer container. It is used by this microservice already: [Reefer container manager](https://github.com/ibm-cloud-architecture/refarch-kc-container-ms/).

## Pre-requisites

Be sure to have set the environment variables in the `./scripts/setenv.sh` to point to your Event Stream or Kafka deployment.

You need to start four terminal windows if you run the solution locally on you laptop, and only 2 terminals if you run the solution on our deployed cluster.

!!! note
        Our deployed cluster in on IBM Cloud Openshift 3.11 cluster.


## Start Reefer container events consumer

In the `consumer` folder use the command:

```
./runContainerConsumer.sh
```

This script starts the docker python image, we built earlier and use the [ConsumeContainers.py](https://github.com/ibm-cloud-architecture/refarch-reefer-ml/blob/master/consumer/ConsumeContainers.py) module.


## Start the predictive scoring service

We can run it locally or on kubernetes cluster like Openshift. Under `scoring` folder, use the command:

```
./runScoringApp.sh
```
In the beginning of the trace log you should see the `bootstrap.servers` brokers list, the `group.id`, and api key as `sasl.password`.

Recalls the scoring is a producer and a consumer.

See the [build and run on Openshift section](https://ibm-cloud-architecture.github.io/refarch-reefer-ml/#scoring:-build-and-run-on-openshift) for running on kubernetes cluster.


## Start the simulator web app

Under the `simulator` folder 

```
./runReeferSimulator.sh
```

To build and run it on Openshift review [this section](#simulator:-build-and-run-on-openshift).

## Start a simulation

Under the `scripts` folder

```
./sendSimulControl.sh 
```

## Validate integration tests

To test your local deployment
```
./sendSimulControl.sh localhost:8080 poweroff
```

or to test on our cloud base deployed solution

```
./sendSimulControl.sh
```

The trace will look like that.

### Simulator trace


### Scoring trace


### Container consumer trace

