from predictservice import PredictService
import os, sys, json
from KcConsumer import KcConsumer
from KcProducer import KcProducer

try:
    KAFKA_BROKERS = os.environ['KAFKA_BROKERS']
except KeyError:
    print("The KAFKA_BROKERS environment variable needs to be set.")
    exit

try:
    KAFKA_APIKEY = os.environ['KAFKA_APIKEY']
except KeyError:
    print("The KAFKA_APIKEY environment variable not set... assume local deployment")

try:
    KAFKA_ENV = os.environ['KAFKA_ENV']
except KeyError:
    KAFKA_ENV='LOCAL'

predictService = PredictService()
producer = KcProducer(KAFKA_ENV,KAFKA_BROKERS,KAFKA_APIKEY,"PredictiveScoringApp")

def processMessage(msg):
    header="""Timestamp, ID, Temperature(celsius), Target_Temperature(celsius), Power, PowerConsumption, ContentType, O2, CO2, Time_Door_Open, Maintenance_Required, Defrost_Cycle"""

    print(msg['payload'])
    score = 0
    if dataAreValid(msg['payload']):
        metric=header+"\n"+msg['payload']
        score = predictService.predict(metric)
    print(score)
    if score == 1:
        print("Go to maintenance " + msg['containerID'])
        tstamp = int(time.time())
        data = {"timestamp": tstamp,
                "type": eventType,
                "version":"1",
                "containerID":  msg['containerID'],
                "payload": {"containerID":  msg['containerID'], 
                    "type": "Reefer",
                    "status": "MaintenanceNeeded",
                    "Reason": "Predictive maintenance scoring found a risk of failure",}
                }
        evt = json.dumps(data)
        producer.publishEvent("containers",evt,"containerID")
    

def dataAreValid(metricStr):
    try:
        metric = eval(metricStr)
    except json.decoder.JSONDecodeError:
        return False
    try:
        for i in range(0,9):
            print(metric[2 + i])
            float(metric[2 + i])
            
    except TypeError or ValueError:
        return False
    return True
    

def startConsumer(predictService):
    print("startConsumer...")
    consumer = KcConsumer(KAFKA_ENV,KAFKA_BROKERS,KAFKA_APIKEY,"containerMetrics",True)
    consumer.prepareConsumer()
    consumer.pollNextEvent(processMessage)
    consumer.close()

if __name__ == "__main__":
    startConsumer(predictService)
