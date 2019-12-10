from flask import Flask, request, jsonify, abort
from flask.cli import FlaskGroup
from flasgger import Swagger
import os, time
from datetime import datetime
from infrastructure.MetricsEventsProducer import MetricsEventsProducer 
from domain.reefer_simulator import ReeferSimulator
from concurrent.futures import ThreadPoolExecutor

'''
created a new FlaskGroup instance to extend the normal CLI with commands related to the Flask app
'''
# use app factory
app = create_app() 

cli = FlaskGroup(create_app=create_app)

swagger_template = {
  "swagger": "2.0",
  "info": {
    "title": "Reefer Simulator",
    "description": "API for health/monitoring and simulation control",
    "contact": {
      "responsibleOrganization": "IBM Garage Solution Engineering",
    },
    "version": "0.1"
  },
  "schemes": [
    "http"
  ],
}


VERSION = "Reefer Container simulator v0.0.10 11/25"
application = Flask(__name__)
swagger = Swagger(application, template=swagger_template)

metricsProducer = MetricsEventsProducer()

# It is considered bad form to return an error for '/', so let's redirect to the apidocs
@application.route('/')
def index():
    return redirect('/apidocs')


@application.route("/health")
def health():
    return VERSION

result = {}
@application.route("/status")
def status():
    return result

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
    
    if nb_records < 500:
        sendEvents(metrics)
    else:
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(sendEvents,metrics)
        
    return jsonify("Simulation started"),202
    

def sendEvents(metrics):
    print(metrics)
    for metric in metrics:
        evt = {"containerID": metric[0],
                "timestamp": str(metric[1]),
                "type":"ReeferTelemetries",
                "payload": str(metric)}
        metricsProducer.publishEvent(evt,"containerID")
    
    
if __name__ == '__main__':
    cli()