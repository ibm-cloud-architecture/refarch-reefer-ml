# Integration tests to proof the solution

Recall that the architecture of the deployed components look like in the figure below. 

![](images/mvp-runtime.png)

So the first component to start is the container consumer which consumer events on the kafka `containers` topic. This is where the microservices will post message about a Reefer container. 

## Start Reefer container events consumer

In the `consumer` folder use the command:

```
./runContainerConsumer.sh
```

This script the docker python image, we built earlier. 

## Start the predictive scoring service

We can run it locally or on kubernetes cluster like openshift. Under `scoring` folder, use the command:

```

```


