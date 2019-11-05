from flask import Flask, request, jsonify, abort
import os, time
from datetime import datetime
from infrastructure.MetricsEventsProducer import MetricsEventsProducer 
from domain.reefer_simulator import ReeferSimulator

VERSION = "Reefer Container simulator v0.0.7 10/29"
application = Flask(__name__)

metricsProducer = MetricsEventsProducer()

@application.route("/")
def hello():
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
    if control["simulation"] == ReeferSimulator.SIMUL_POWEROFF:
        metrics=simulator.generatePowerOffTuples(control["containerID"],int(control["nb_of_records"]),control["product_id"])
    elif  control["simulation"]  == ReeferSimulator.SIMUL_CO2:
        metrics=simulator.generateCo2Tuples(control["containerID"],int(control["nb_of_records"]),control["product_id"])
    elif  control["simulation"]  == ReeferSimulator.SIMUL_O2:
        metrics=simulator.generateO2Tuples(control["containerID"],int(control["nb_of_records"]),control["product_id"])
    else:
        return jsonify("Wrong simulation controller data"),404
    
    for metric in metrics:
        evt = {"containerID": control["containerID"],
                "timestamp": str(metric[0]),
                "type":"ReeferTelemetries",
                "payload": str(metric)}
        metricsProducer.publishEvent(evt,"containerID")
    return "Simulation started"
    

if __name__ == "__main__":
    print(VERSION)
    application.run()
    
