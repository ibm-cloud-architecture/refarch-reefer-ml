# Reefer ML Simulator _(simulator)_

The _simulator_ component is a Python-based application for generating anomalous data events for refrigerated shipping containers (also known as 'reefers').

## Installation

The application is built using [Appsody](https://appsody.dev) as the developer experience tooling.  The Appsody CLI is required locally to build and deploy the application properly, while the Appsody Operator is required on the target cluster to deploy the generated `AppsodyApplication`.

### Docker build

The Docker image can be built from this directory by using the `appsody build` command:

1. Ensure you are logged in to the desired remote Docker registry through your local Docker client.
2. The `appsody build -t ibmcase/kcontainer-reefer-simulator:appsody-v1 --push` command will build and push the application's Docker image to the specified remote image registry.

### Application deployment

The application can be deployed to a remote OpenShift cluster by using the `appsody deploy` command:
1. There are three required configuration elements for connectivity to IBM Event Streams (Kafka) prior to deployment:
  - A `ConfigMap` named `kafka-brokers` **[Reference Link](https://ibm-cloud-architecture.github.io/refarch-kc/deployments/backing-services/#event-streams-kafka-brokers_1)**
  - A `Secret` named `eventstreams-api-key` **[Reference Link](https://ibm-cloud-architecture.github.io/refarch-kc/deployments/backing-services/#event-streams-api-key_1)**
  - A `Secret` named `eventstreams-cert-pem` _(if connecting to an on-premise version of IBM Event Streams)_ **[Reference Link](https://ibm-cloud-architecture.github.io/refarch-kc/deployments/backing-services/#event-streams-certificates)**

## Usage

Once deployed, you can access the Swagger-based REST API via the defined route and trigger the simulation controls.

1. To determine the route, use the `oc get route reefer-simulator` command and go to the URL specified in the `HOST/PORT` field in your browser.
2. From there, drill down into the `POST /control` section and click **Try it out!**.
3. Enter any of the following options for the fields prepopulated in the `control` body:
  - Container: `C01, C02, C03, C04`
  - Product: `P01, P02, P03, P04`
  - Simulation: `poweroff, co2sensor, o2sensor, normal`
  - Number of records: A positive integer
4. Click **Execute**

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
