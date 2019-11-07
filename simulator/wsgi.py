from flask import Flask, request, jsonify, abort
import os, time
from datetime import datetime
from infrastructure.MetricsEventsProducer import MetricsEventsProducer 
from domain.reefer_simulator import ReeferSimulator
from concurrent.futures import ThreadPoolExecutor

VERSION = "Reefer Container simulator v0.0.9 11/06"
application = Flask(__name__)

metricsProducer = MetricsEventsProducer()

@application.route("/")
def hello():
    return VERSION

@application.route("/health")
def health():
    return VERSION

# Need to support asynchronous HTTP Request, return 202 accepted while starting 
# the processing of generating events. The HTTP header needs to return a
# location to get the status of the simulator task    
@application.route("/control", methods = ['POST'])
def runSimulator():
    print("post received: ")
    print(request.json)
    if not 'containerID' in request.json:
        abort(400) 
    control = request.json
    simulator = ReeferSimulator()
    nb_records = int(control["nb_of_records"])
    if control["simulation"] == ReeferSimulator.SIMUL_POWEROFF:
        metrics=simulator.generatePowerOffTuples(control["containerID"],nb_records,control["product_id"])
    elif  control["simulation"]  == ReeferSimulator.SIMUL_CO2:
        metrics=simulator.generateCo2Tuples(control["containerID"],nb_records,control["product_id"])
    elif  control["simulation"]  == ReeferSimulator.SIMUL_O2:
        metrics=simulator.generateO2Tuples(control["containerID"],nb_records,control["product_id"])
    else:
        return jsonify("Wrong simulation controller data"),404
    
    with ThreadPoolExecutor() as executor:
        executor.submit(sendEvents,metrics)
        
    return jsonify("Simulation started"),202
    

def sendEvents(metrics):
    for metric in metrics:
        evt = {"containerID": metric[0],
                "timestamp": str(metric[1]),
                "type":"ReeferTelemetries",
                "payload": str(metric)}
        metricsProducer.publishEvent(evt,"containerID")
    

if __name__ == "__main__":
    print(VERSION)
    application.run()
    
