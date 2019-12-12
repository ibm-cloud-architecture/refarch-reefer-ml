# Event Streams provisioning and configuration

We cover a lot about Kafka installation and configuration in the [EDA reference architecture repository](https://ibm-cloud-architecture.github.io/refarch-eda/). 

## Deploying Event Streams from CP for integration

The [cloud pack for integration](https://www.ibm.com/cloud/cloud-pak-for-integration) includes IBM Event Streams, the Kafka solution for on premise deployment. 

Once you have an Openshift cluster, you can install cloud pak for integration as presented in [this tutorial](https://cloudpak8s.io/integration/onprem/#run-the-integration-cloud-pak-install).

Then you can deploy Event streams with a 3 brokers cluster using the CP4I home page:

![](images/cp4i-home-es.png)

using the steps described in [this tutorial](https://cloudpak8s.io/integration/deploy-kafka/). 


We also use the [Event Streams product documentation](https://ibm.github.io/event-streams/installing/installing-openshift/).

## Defines topics

The following diagram illustrates the needed Kafka topics configured in IBM Cloud Event Stream service:

![](images/es-topics.png)

As an alternate you can use Event Streams on Public Cloud.

## IBM Cloud Public

We recommend creating the Event Stream service using the [IBM Cloud catalog](https://cloud.ibm.com/catalog/services/event-streams), you can also read our [quick article](https://ibm-cloud-architecture.github.io/refarch-eda/deployments/eventstreams/es-ibm-cloud/) on how to deploy Event Streams. 


With IBM Cloud deployment use the service credentials to create new credentials to get the Kafka brokers list, the admin URL and the api key needed to authenticate the consumers and the producers.

For Event Streams on Openshift deployment, click to the `connect to the cluster` button to get the broker URL and to generate the API key: select the option to generate the key for all topics.

![](images/cluster-access.png)

