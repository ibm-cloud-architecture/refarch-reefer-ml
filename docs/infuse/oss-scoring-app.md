# Scoring app using Python

In this article we are presenting how to develop the scoring agent using python and serialized model, developed with Jupiter notebook.

## Requirements

We are using the [job stories](https://jtbd.info/replacing-the-user-story-with-the-job-story-af7cdee10c27) to define the requirements:

1. when a Reefer container telemetry event arrives, I want the scoring app to compute an anomaly detection predictive score so that it can create a reefer container maintance command event.
1. when a Reefer container telemetry event arrives, I want the scoring app I want the data to be transform so the scoring can be done using expected structure.
1. when the scoring app is deploy to kubernetes, I want to be sure it is healthy so that the kubernetes scheduler does not kill it


## Create the project with Appsody

*For this code we are using the same approach as for the simulator app development*



The application is built using [Appsody](https://appsody.dev) as the developer experience tooling. The [Appsody CLI](https://appsody.dev/docs/getting-started/installation) is required locally to build and deploy the application properly.


## Code approach

* Flask
* blueprint
* swagger 


## Integrate test driven development

* [pyttest]()
* [Coverage]()

## Deployent to openshift

* appsody deploy

## Code explanation
