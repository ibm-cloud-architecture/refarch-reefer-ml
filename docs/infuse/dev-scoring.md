# Develop the scoring agent with cloud pak for application

We have two approaches to build the predictive scoring agent: 

1. one using a python Flask app listening to telemetry events coming from Kafka, run the predictive scoring within the same app. The model was developed with Jupiter notebook and serialized with [pickle](https://docs.python.org/3/library/pickle.html), so it responds in microseconds and generates anomaly to a second kafka topic. The code is under `scoring` folder, and uses essentially open source components. See [this article](oss-scoring-app.md) to understand how it is built.
1. one using Java microprofile 3.0 with the reactive messaging annotations, to consume telemetry events and call a remote predictive scoring service, developped and deployed within Cloud Pak for Data. The code is under `scoping-mp` folder.

The scoring service needs to use an analytics scoring model built using a machine learning techniques, and serialized so that it can be loaded in memory.


## Java Micro Profile 3.0 with Cloud Pak for Application

In this implementation we use the [Appsody](https://appsody.dev/) Java microprofile stack to create the project template and deploy with appsody CLI. 
As the `scoring-mp` component is consuming message from Kafka and produce messages, we want to use the Reactive messaging extension to microprofile. We are reusing the approach presented in [this repository](https://github.com/Emily-Jiang/reactive-service-a) based on [SmallRye Reactive Messaging](https://smallrye.io/smallrye-reactive-messaging/).


## Deploying the model using Watson Machine Learning

TODO Cloud Pak model deployment

## Further Readings

* [Appsody for cloud native development](https://appsody.dev/)
* [Appsody microprofile stack](https://github.com/appsody/stacks/tree/master/incubator/java-microprofile)
* [Cloud Pak for Application demo video](https://www.youtube.com/watch?v=cKIkhhONBKM&t=46s)
* [Use Codewind for VScode](https://www.eclipse.org/codewind/mdt-vsc-getting-started.html)