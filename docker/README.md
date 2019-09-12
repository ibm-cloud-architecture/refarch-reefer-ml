# Run the solution locally for development purpose

## Build each images

* For simulator as web application:

    ```
    cd simulator
    docker build . -t ibmcase/reefersimulator
    ```

* For container tracer

    ```
    cd consumer
    docker build . -t ibmcase/containerconsumer
    ```

* For scoring as web app
    ```
    cd scoring/webapp
    docker build . -t ibmcase/predictivescoringweb
    ```

* For scoring as kafka listener and producer
    ```
    cd scoring/eventConsumer
    docker build . -t ibmcase/predictivescoring
    ```

## Running the solution locally

* Start the kafka and zookeeper

Under the docker folder
```
docker-compose -f backbone-compose.yml up &
```

* The first time you start kafka add the different topics needed for the solution:

```
./scripts/createTopics.sh LOCAL
```

* Start the solution 

```
docker-compose -f solution-compose.yml up &
```

* To stop and clean everything

```
docker-compose -f solution-compose.yml down
docker-compose -f backbone-compose.yml down
```

* You can also remove the kafka1 and zookeeper1 folders under docker. If you do so be sure to recreate the topics.

## Testing the solution

* Send a simulation control json to the simulator: under the `scripts` folder

```
./sendSimulControl.sh localhost:8080 co2sensor C101
```

