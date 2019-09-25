from flask import Flask, request, jsonify, abort
import os, time
from datetime import datetime
from infrastructure.MetricsEventsProducer import MetricsEventsProducer 
from domain.reefer_simulator import ReeferSimulator

VERSION = "Reefer Container simulator v0.0.4"
application = Flask(__name__)

metricsProducer = MetricsEventsProducer()

@application.route("/")
def hello():
    return VERSION
    
@application.route("/control", methods = ['POST'])
def runSimulator():
    print("post received: ")
    print(request.json)
    if not 'containerID' in request.json:
        abort(400) 
    control = request.json
    simulator = ReeferSimulator()
    if control["simulation"] == ReeferSimulator.SIMUL_POWEROFF:
        metrics=simulator.generatePowerOffTuples(control["containerID"],int(control["nb_of_records"]),float(control["good_temperature"]))
    elif  control["simulation"]  == ReeferSimulator.SIMUL_CO2:
        metrics=simulator.generateCo2Tuples(control["containerID"],int(control["nb_of_records"]),float(control["good_temperature"]))
    else:
        return "Wrong simulation controller data"
    
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
    
