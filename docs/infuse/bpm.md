# Maintenance field engineer dispatching business process

Need to cover:

* problem statement
* business process model
* deploy to BPM on cloud
* service end point explanation
* specific logic in the container microservice
* demonstration script for a BPM point of view 

## Problem statement

When the anomaly detection scoring service create a maintenance record on the containers topic, the container microservice will trigger a field engineer dispatching case so an engineer can go the reefer container if it was unloaded in the destination harbor. 

Before creating a ticket or while adding information to the ticket, the process may get the container estimated arrival time and destination harbor to do the dispatching. This mean adding an API on container microservice.

