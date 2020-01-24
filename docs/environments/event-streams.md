# Event Streams provisioning and configuration

We cover a lot about Kafka or IBM Event Streams installation and configuration in the [EDA reference architecture repository](https://ibm-cloud-architecture.github.io/refarch-eda/deployments/eventstreams/). In this short note we just highlight the steps to be done for deploying Event Streams on premise using Cloud Pak for integration.

## Deploying Event Streams from Cloud Pak for Integration

The [cloud pack for integration](https://www.ibm.com/cloud/cloud-pak-for-integration) includes IBM Event Streams, the Kafka solution for on premise deployment.

Once you have an Openshift cluster, you can install cloud pak for integration as presented in [this tutorial](https://cloudpak8s.io/integration/onprem/#run-the-integration-cloud-pak-install). Then you can deploy Event streams with the default configuration of three broker cluster from the CP4I home page:

![](images/cp4i-home-es.png)

![](images/es-ocp-instance.png)

For your own deployment you can follow the steps described in [this tutorial](https://cloudpak8s.io/integration/deploy-kafka/) and the [Event Streams product documentation](https://ibm.github.io/event-streams/installing/installing-openshift/).

Once you have your instance up and running, you need to get the URL for the brokers, the API key to access topics and the TLS certificate.

![](images/es-ocp-cluster-conn.png)

Define the API key:

![](images/es-ocp-api-key-res.png)

![](images/es-ocp-api-key.png)

The copy the broker URL and api key in the `scripts/setenv.sh` file under the OCP choice:

```
OCP)
    export KAFKA_BROKERS=eventstream140-ibm-es-proxy-route-bootstrap-eventstreams.apps.green.ocp.csplab.local:443
    export KAFKA_APIKEY="zb5Rv-81m11A0_"
    export KAFKA_CERT="/project/useapp/simulator/certs/ocp/es-cert.pem"
```

And then download the pem and java key. We keep those files in the `certs/ocp` folder.

As an alternate you can use Event Streams on Public Cloud.


## Event Streams on IBM Cloud Public

We recommend creating the Event Stream service using the [IBM Cloud catalog](https://cloud.ibm.com/catalog/services/event-streams), you can also read our [quick article](https://ibm-cloud-architecture.github.io/refarch-eda/deployments/eventstreams/es-ibm-cloud/) on how to deploy Event Streams.


With IBM Cloud deployment use the service credentials to create new credentials to get the Kafka brokers list, the admin URL and the api key needed to authenticate the consumers and the producers.

For Event Streams on Openshift deployment, click to the `connect to the cluster` button to get the broker URL and to generate the API key: select the option to generate the key for all topics.

![](images/cluster-access.png)


## Defines topics

### Create Kafka topics through Kubernetes Job automation

In an effort to keep development systems as clean as possible and speed up deployment of various scenarios, our deployment tasks have been encapsulated in [Kubernetes Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/). These are runnable on any Kubernetes platform, including OpenShift.

1. Following the configuration prerequisistes defined in the [Backing Services](https://ibm-cloud-architecture.github.io/refarch-kc/deployments/backing-services/) documentation for using Kafka via [IBM Event Streams on IBM Cloud](https://ibm-cloud-architecture.github.io/refarch-kc/deployments/backing-services/#using-ibm-event-streams-hosted-on-ibm-cloud) or [IBM Event Streams on OpenShift](https://ibm-cloud-architecture.github.io/refarch-kc/deployments/backing-services/#using-ibm-event-streams-deployed-on-redhat-openshift-container-platform), you should already have the following Kubernetes ConfigMap & Secrets defined in your target namespace with the information available from the **Connect to this service** tab on the respective Event Streams service console:
    1. **ConfigMap:** `kafka-brokers` _(in a comma-separated list)_
      ```shell
      kubectl create configmap kafka-brokers --from-literal=brokers='host1.appdomain.cloud.com,host2.appdomain.cloud.com,...'
      ```
    2. **Secret:** `eventstreams-apikey`
      ```shell
      kubectl create secret generic eventstreams-apikey --from-literal=binding='1a2...9z0'
      ```
    3. **Secret:** `eventstreams-truststore-jks` _(this is only required when connecting to IBM Event Streams on OpenShift)_
      ```shell
      kubectl create secret generic eventstreams-truststore-jks --from-file=~/Downloads/es-cert.jks
      ```
    4. **Event Streams Truststore password** - this value is not contained in a Kubernetes Secret, but if using non-default settings in the Event Streams deployment, it should be verified that the password for the generated truststore file is still the default value of `password`.

2. Review the `/scripts/createKafkaTopics.yaml` and the fields contained in the `env` section for optional parameters that can be modified when running the Job for non-default tasks.

3. Create the `create-kafka-topics` Job from the root of the `refarch-reefer-ml` repository:
```shell
kubectl apply -f scripts/createKafkaTopics.yaml
```

4. You can tail the created pod's output to see the progress of the Kafka topic creation:
```shell
kubectl logs -f --selector=job-name=create-kafka-topics
```

### Create Kafka topics manually through offering UI

The following diagram illustrates the needed Kafka topics configured in IBM Cloud Event Stream service:

![](images/es-topics.png)

For the telemetries we are now using 3 replicas. This is an example of configuration for Event Streams on openshift on premise:

![](images/ocp-es-topics.png)
