# IBM Cloud Pak for Data: data collection

To develop the anomaly predictive service we first need to access the data. We have two datasources in this example: the product information and the telemetries data coming from the different Reefer Containers. With the telemetries we should be able to assess anomaly. The Telemetries are saved to a noSQL database. We are using MongoDB on IBM Cloud.


## Create a new project

Once logged into Cloud Pak for Data, create a new project. From the main page select the project view: 

![](images/create-project-0.png)

and then new project, and select `analytics`:

![](images/create-project-1.png)

Select an empty project: 

![](images/create-project-2.png)

Enter basic information about your project

![](images/create-project-3.png)

The result is the access to the main project page:

![](images/create-project-4.png)

Now we need to define data source...

## Data Virtualization

To do not copy or move the data, we can add `Data virtualization` to a remote data source. 
First we need to get the connection information for the MongoDB database. Going to the IBM Cloud account, under the Services resource, select the mongo instance:

![](images/ibm-cloud-res-mongo.png)

And get the information about the data connection.

![](images/mongo-connection.png)

And download the TLS certificate as pem file:

```shell
ibmcloud login -a https://cloud.ibm.com -u passcode -p <somecode-you-get-from-your-login>
# Define your resource group
ibmcloud target -g gse-eda
ibmcloud cdb deployment-cacert gse-eda-mongodb > certs/mongodbca.pem
```

Back to Cloud pak for data, an administrator can define a connection as a reusable object by entering the data source information. The figure below illustrates the configuration for the Mongo DB on IBM Cloud:

![](images/add-connection.png)

Once done a Data scientist can define in the Collect menu a new `Data virtualization`



