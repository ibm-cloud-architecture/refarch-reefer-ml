from domain.predictservice import PredictService
import  json, time
from infrastructure.MetricsEventListener import MetricsEventListener
from infrastructure.ContainerEventsProducer import ContainerEventsProducer

predictService = PredictService()
containerEventsProducer = ContainerEventsProducer()

def assessPredictiveMaintenance(msg):
    header="""Timestamp, ID, Temperature(celsius), Target_Temperature(celsius), Power, PowerConsumption, ContentType, O2, CO2, Time_Door_Open, Maintenance_Required, Defrost_Cycle"""

    print(msg['payload'])
    score = 0
    if assessDataAreValid(msg['payload']):
        metricValue = msg['payload'].replace('(','').replace(')','')
        metric = header+"\n"+metricValue
        score = predictService.predict(metric)
    print(score)
    if score == 1:
        print("Go to maintenance " + msg['containerID'])
        tstamp = int(time.time())
        data = {"timestamp": tstamp,
                "type": "ContainerMaintenance",
                "version":"1",
                "containerID":  msg['containerID'],
                "payload": {"containerID":  msg['containerID'], 
                    "type": "Reefer",
                    "status": "MaintenanceNeeded",
                    "Reason": "Predictive maintenance scoring found a risk of failure",}
                }
        containerEventsProducer.publishEvent(data,"containerID")
    

def assessDataAreValid(metricStr):
    try:
        metric = eval(metricStr)
    except json.decoder.JSONDecodeError:
        return False
    try:
        for i in range(0,9):
            float(metric[2 + i])
            
    except TypeError or ValueError:
        return False
    return True
    

def startReeferMetricsEventListener():
    print("startReeferMetricsEventListener(  groupid = reefermetricsconsumer") 
    metricsEventListener = MetricsEventListener()
    metricsEventListener.processEvents(assessPredictiveMaintenance)
    return metricsEventListener
    

if __name__ == "__main__":
    print("Reefer Container Predictive Maintenance Scoring Service v0.0.3")
    metricsEventListener = startReeferMetricsEventListener()
    metricsEventListener.close()
