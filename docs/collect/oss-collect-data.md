
As part of the IBM AI ladder practice introduced in the [Data  AI reference architecture](https://ibm-cloud-architecture.github.io/refarch-data-ai-analytics) and specially the collect step, we need to get a data topology in place to get data at rest so data scientist can do their data analysis, and feature preparation.

In this solution, there are two datasources:

* the events in the kafka topic, using the [event sourcing design pattern](https://ibm-cloud-architecture.github.io/refarch-eda/design-patterns/event-sourcing/).
* the database about the Reefer, the fresh products and reefer telemetries

As we do not have Reefer telemetry public data available, we are using our simulator to develop such data. The figure below illustrates this data injection simulation.

![](images/data-collect.png)

***Also you can use the simulator to create data in csv file, so there is no need to use postgresql to develop the model.***
