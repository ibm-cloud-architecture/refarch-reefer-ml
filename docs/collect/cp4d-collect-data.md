# IBM Cloud Pak for Data: data collection

To develop the anomaly predictive service we first need to access the data. We have two datasources in this example: the product information and the telemetries data coming from the different Reefer Containers. With the telemetries we should be able to assess anomaly. The Telemetries are saved to a noSQL database. We are using MongoDB on IBM Cloud.

Using [Mongo Compass](../environments/mongodb-compass.md), we can see one of telemetry document as saved into MongoDB.

![Telemetries in Mongo](images/telemetry-mongo.png)
**Figure 1: Mongo DB Compass: ibmcloud.telemetries collection**

It is important to note that the Json document has sensors document embedded. As we will see later they will be mapped to different tables in Cloud Pak Virtualization.

As part of the data governance capability, a user with data engineer role can do the following tasks:

* Define one to many connections to the remote different data sources
* Create virtual assets to materialize tables and views from the different data sources
* Assign an asset to an exisint project or a data request (governance object to ask to access data)

## Define connection

First we need to get the connection information for the MongoDB database. See [this note](../environments/mongo.md) for information about Mongo DB instance on IBM Cloud.


* Get the information about the data connection.

![Mongo connection](images/mongo-connection.png)
**Figure 2: Mongo DB on IBM Cloud connection information**

* Then download the TLS certificate as pem file:

```shell
ibmcloud login -a https://cloud.ibm.com -u passcode -p <somecode-you-get-from-your-login>
# Define your resource group
ibmcloud target -g gse-eda
ibmcloud cdb deployment-cacert gse-eda-mongodb > certs/mongodbca.pem
```

Back to Cloud pak for Data, an administrator may define connections as a reusable objects by entering the data sources information. The figure below illustrates the connection configuration to the Mongo DB running on IBM Cloud:

![CP4D add connection](images/add-connection.png)
**Figure 3: Define connection in CP4D**

**Add connection in Cloud Pak for Data**

. Virtualization can help automatically group tables, so it simplifies to group different data elements into a single schema.

Once define a Data scientist use this connection in the Collect menu to define a new `Data virtualization` definition to discover the telemetries data.

## Create a new project

Once logged into Cloud Pak for Data, create a new project. A project is a collection of assets the analytics team work on. It can include data assets and Notebooks, RStudio files
Models, scripts...

From the main page select the project view:

![Analytic project](images/create-project-0.png)

and then new project, and select `analytics`:

![](images/create-project-1.png)

Select an empty project:

![](images/create-project-2.png)

Enter basic information about your project

![](images/create-project-3.png)

The result is the access to the main project page:

![](images/create-project-4.png)

Now we need to define data assets into our project...

## Data Virtualization

As introduced in [this paragraph](https://ibm-cloud-architecture.github.io/refarch-data-ai-analytics/architecture/collect-org-data/), we want to use data virtualization to access the historical telemetries records. The data engineer uses the `Data virtualization` capability to search for existing tables and add the tables he wants in the `cart`. For that, he uses the `Virtualize` menu 

![](images/virtualize-1.png)

and then selects mongodb in the `Filters` column and may be apply some search on specific database name. 

![](images/virtualization.png)

Once done, he selects the expected tables and then use `Add to cart` link. It is important to note that we have two tables to match the telemetry json document and the sensors sub json document.

The next step is to assign them to a project:

![](images/virtualize-tables.png)

## Create a joined view

We need to join the telemetries and the sensors data into the same table, to flatten the records. As there is 1 to 1 relationship as of now.
In the Data Virtualization, a data steward selects `My Virutalized data`, and then 
select TELEMETRIES and TELEMETRY_SENSORS tables, then the `Join view`. Within this new panel, he needs to create a join key, by drag the `TELEMETRICS_ID` and `_ID` together:

![](images/join-tables.png)

Once joined and the view is created, he can get those new assets as part of his project.

![](images/telemetries-asset.png)

Next is to start working within a model [--> Next -->](../analyze/ws-ml-dev.md)