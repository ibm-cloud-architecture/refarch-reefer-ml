from domain.predictservice import PredictService
import  json, time, os
from infrastructure.MetricsEventListener import MetricsEventListener
from infrastructure.ContainerEventsProducer import ContainerEventsProducer

'''
Scoring agent is a event consumer getting Reefer telemetry or metrics. For each event
received it assesses if there is a need to do a maintenance on this reefer due to strange
metrices
'''

predictService = PredictService()
containerEventsProducer = ContainerEventsProducer()


def assessPredictiveMaintenance(msg):
    '''
    Call back used by the event consumer to process the event. 

    Argument the message as dict / json format to preocess.
    In the case of maintenance needed, generate an event to the containers topic
    '''
    header = """container_id, timestamp, product_id, temperature, target_temperature, ambiant_temperature, kilowatts, time_door_open, content_type, defrost_cycle, oxygen_level, nitrogen_level, humidity_level, carbon_dioxide_level, vent_1, vent_2, vent_3, maintenance_required"""
    print(msg['payload'])
    score = 0
    if assessDataAreValid(msg['payload']):
        metricValues = msg['payload'].replace('(','').replace(')','')
        metric = header+"\n"+metricValues
        score = predictService.predict(metric)
    print(score)
    if score == 1:
        # TODO do not send a maintenance event if already done in the current travel.
        # This will lead to a stateful agent...
        tstamp = int(time.time())
        metricValues = eval(msg['payload'])
        data = {"timestamp": tstamp,
                "type": "ContainerMaintenance",
                "version":"1",
                "containerID":  msg['containerID'],
                "payload": {
                    "timestamp": metricValues[0],
                    "containerID": metricValues[1],
                    "temperature": metricValues[2],
                    "target_temperature": metricValues[3],
                    "ambiant_temperature": metricValues[4],
                    "kilowatts": metricValues[5],
                    "content_type" : metricValues[6],
                    "oxygen_level" : metricValues[7],
                    "nitrogen_level" : metricValues[8],
                    "carbon_dioxide_level" : metricValues[9],
                    "humidity_level" : metricValues[10],
                    "latitude": "37.8226902168957",
                    "longitude": "-122.3248956640928",
                    "vent_1": metricValues[11],
                    "vent_2" : metricValues[12],
                    "vent_3" : metricValues[13],
                    "time_door_open" : metricValues[14],
                    "defrost_cycle": metricValues[15]
                }
            }
        print(data)
        containerEventsProducer.publishEvent(data,"containerID")
    

def assessDataAreValid(metricStr):
    try:
        metric = eval(metricStr)
    except json.decoder.JSONDecodeError:
        print("Not able to decode")
        return False
    try:
        for i in range(0,9):
            float(metric[3 + i])
    except TypeError or ValueError:
        return False
    return True
    

def startReeferMetricsEventListener():
    print("startReeferMetricsEventListener(  groupid = reefermetricsconsumer") 
    metricsEventListener = MetricsEventListener()
    metricsEventListener.processEvents(assessPredictiveMaintenance)
    return metricsEventListener
    

if __name__ == "__main__":
    '''
    Just start the event listener
    '''
    print("Reefer Container Predictive Maintenance Scoring Agent v0.0.6 10/21")
    metricsEventListener = startReeferMetricsEventListener()
    metricsEventListener.close()
