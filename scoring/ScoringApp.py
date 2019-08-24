from predictservice import PredictService
import os,sys
from KcConsumer import KafkaConsumer

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

def processMessage(msg):
    header="""Timestamp, ID, Temperature(celsius), Target_Temperature(celsius), Power, PowerConsumption, ContentType, O2, CO2, Time_Door_Open, Maintenance_Required, Defrost_Cycle"""
    metric=header+"\n"+msg['payload']
    print(metric)
    score = predictService.predict(metric)
    print(score)
    if score == 1:
        print("Go to maintenance " + msg['containerID'])
    


def startConsumer(predictService):
    print("startConsumer...")
    consumer = KafkaConsumer(KAFKA_ENV,KAFKA_BROKERS,KAFKA_APIKEY,"containerMetrics",False)
    consumer.prepareConsumer()
    consumer.pollNextEvent(processMessage)
    consumer.close()

if __name__ == "__main__":
    
    startConsumer(predictService)
