# Reefer Container Predictive Maintenance

In this section, we discuss how to build an analytic model using machine learning techniques from data coming from event store like kafka. We train the model with the help of historical data to predict whether maintenance is required for the reefer container at a certain point in time.

You will learn how to simulate date for reefer, develop the predictive maintenance model, and integrate the model into an application.

## Introduction

A reefer container is a refrigerated shipping container used to store or transport frozen or cold goods perishable items or goods that require temperature control. 

![Reefer](images/reefer.png)

Reefers make an excellent, portable solution for short or long term storage and can be used to ship or truck goods over long distances as they can be plugged into the power station on ships or have it clipped on generators attached.

Perishable products must be kept at a controlled temperature, from point of origin to delivery to retailer or pharmacy. The logistics industry refers to this as the “cold chain” and it encompasses both “reefers” (refrigerated containers) as well as warehouses, distribution centers and the final storage or holding areas.

Throughout this chain the risk of failure is ever-present, meaning there is always a possibility of cargo exceeding permissible or safe temperature levels, even if only briefly. For example, a truck might be stopped without power in desert heat, allowing temperatures in the reefer to rise. Then power is restored and the temperature in the container comes back down, but the product is damaged.

When cargo with such as any of those items listed above are exposed to temperatures outside of prescribed limits it can be damaged. In some cases this is evident, such as with bananas, but in other situations, like the transport of vaccines, it may not be apparent that damage has occurred and the vaccine becomes ineffective. For some products, going over temperature, even only briefly, can reduce shelf life dramatically, incurring substantial costs when it cannot be sold. 

Organizations contracting to ship perishable products often specify the permissible temperature range. However, even if it is possible to show that product was exposed to conditions outside of those contracted, proving where it happened, and thus responsibility, can be much harder.

## Predictive maintenance problem statement

The success of predictive maintenance models depend on three main components: 

* having the right data
* framing the problem appropriately 
* evaluating the predictions properly

From a methodology point of view the Data Scientist needs to address the following questions:

* What type of failure to consider and which one to predict?
* What kind of failure is happening? slow degradation or instantaneous failure?
* What could be the relation between a product characteristics and the failure?
* What kind of measure exist to assess the given characteristic?
* Which measurements correspond to good functioning and which ones correspond to failure?
* How often metrics are reported?
* What question the model should answer?
* What kind of output should the model give?
* How long in advance should the model be able to indicate that a failure will occur?
* What are the business impact to do not predict the failure? and predicting false negative failure?
* What is the expected accuracy?  

### Reefer problem types

There are multiple different potential issues that could happen to a refrigerator container. We are choosing to model the "Sensor Malfunctions" issue: Sensors in the refrigeration unit need to be calibrated and be continuously operational. An example of failure may come from the air sensor making inaccurate readings of temperatures, which leads to sploiled content. A potential reason may come from a faulty calibration, which can go unnoticed for a good time period. It may be difficult to know if there is an issue or not. 

The other common potential issues are:

* Fluid leaks, like engine oil, coolant liquid. The preassure sensors added to the circuit may help identify preassure lost over time.
* Faulty belts and hoses.
* Faulty calibration: A non-calibrated reefer can cool at a slower or faster rate than desired.
* Damaged Air Chute.
* Condenser Issues like broken or damaged coils, clamps or bolts missing, and leaks.
* Door Seals damaged. 
* Blocked air passage: to keep the temperature homogenous inside the reefer.

So the question we want to answer is: does the Reefer keep accurate temperature overtime between what is set versus what is measured?

## Modeling techniques

The model uses the generated data from above scenarios: 

1. When the container's door is open for a longer time - this gives a false positive that maintainence is required.
1. When sensors are malfunctioning, it records arbitrary readings.
1. When the readings are normal. We have currently trained our model on 3000 datapoints from the three scenarios above. 

There are different modeling approach to tackle predictive maintenance:

* regression model
* classification to predict failure for a given time period
* classify anomalous behavior: classes are not known in advance. Normal operation is known.
* compute probability of failure over time

### Code execution

The simulator continuosly generates container metrics, publishes it to Kafka and run the predictMaintainence.ipynb to predict if maintainence is sought at this point in time. 

## Model description

We are using Machine Learning supervised learning here. There are two types of supervised learning - 1) Classification: Predict a categorical response, 2) Regression: Predict a continuous response

### Linear regression

Pros: 1) Fast 2) No tuning required 3) Highly interpretable 4) Well-understood

Cons: 1) Unlikely to produce the best predictive accuracy 2) Presumes a linear relationship between the features and response 3) If the relationship is highly non-linear as with many scenarios, linear relationship will not effectively model the relationship and its prediction would not be accurate

### Naive Bayes classification

Naive Bayes is a probabilistic classifier inspired by the Bayes theorem under a simple assumption which is the attributes are conditionally independent.

The classification is conducted by deriving the maximum posterior which is the maximal P(Ci|X) with the above assumption applying to Bayes theorem. This assumption greatly reduces the computational cost by only counting the class distribution. Even though the assumption is not valid in most cases since the attributes are dependent, surprisingly Naive Bayes has able to perform impressively.

Naive Bayes is a very simple algorithm to implement and good results have obtained in most cases. It can be easily scalable to larger datasets since it takes linear time, rather than by expensive iterative approximation as used for many other types of classifiers.

Naive Bayes can suffer from a problem called the zero probability problem. When the conditional probability is zero for a particular attribute, it fails to give a valid prediction. This needs to be fixed explicitly using a Laplacian estimator.



## Model evaluation

We are using Root Mean Squared Error (RMSE) for evaluating the model performance.

Root Mean Squared Error (RMSE) is the square root of the mean of the squared errors.

Classification does better here as the scenarion is more of a classification problem.

## References


* [Understand Reefer container](https://cargostore.com/blog/what-are-reefer-containers/)
* For modeling predictive maintenance we found [this article](https://medium.com/bigdatarepublic/machine-learning-for-predictive-maintenance-where-to-start-5f3b7586acfb) from BigData Republique, on Medium, very interesting. 
* [PREDICTION OF TEMPERATURE INSIDE A REFRIGERATED CONTAINER IN THE PRESENCE OF PERISHABLE GOODS](http://www.sfb637.uni-bremen.de/pubdb/repository/SFB637-B6-10-011-IC.pdf)
* [Temperature Monitoring During Transportation, Storage and Processing of Perishable Products](https://www.omega.com/technical-learning/temperature-monitoring-during-transportation.html)

* [Understanding machine learning classifiers](https://towardsdatascience.com/machine-learning-classifiers-a5cc4e1b0623)