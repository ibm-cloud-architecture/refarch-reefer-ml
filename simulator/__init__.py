from flask import Flask, redirect, request, jsonify, abort
from server import app
from server.routes.prometheus import track_requests
import os, time
from datetime import datetime
from userapp.infrastructure.MetricsEventsProducer import MetricsEventsProducer 
from userapp.domain.reefer_simulator import ReeferSimulator
from concurrent.futures import ThreadPoolExecutor

# The python-flask stack includes the flask extension flasgger, which will build
# and publish your swagger ui and specification at the /apidocs url. Here we set up
# the basic swagger attributes, which you should modify to match you application.
# See: https://github.com/rochacbruno-archive/flasgger
swagger_template = {
  "swagger": "2.0",
  "info": {
    "title": "Reefer Simulator for Telemetry generation",
    "description": "API for controlling the simulation, plus health/monitoring",
    "contact": {
      "responsibleOrganization": "IBM",
      "email": "boyerje@us.ibm.com",
      "url": "https://ibm-cloud-architecture.github.io",
    },
    "version": "0.1"
  },
  "schemes": [
    "http"
  ],
}
swagger = Swagger(app, template=swagger_template)
metricsProducer = MetricsEventsProducer()
# The python-flask stack includes the prometheus metrics engine. You can ensure your endpoints
# are included in these metrics by enclosing them in the @track_requests wrapper.

# Need to support asynchronous HTTP Request, return 202 accepted while starting 
# the processing of generating events. The HTTP header needs to return a
# location to get the status of the simulator task    
@app.route("/control", methods = ['POST'])
@track_requests
def runSimulator():
    """Control the reefer telemetry simulation
    ---
    requestBody:
        required: true
        content:
          application/json:
            schemas:
              Control:
                title: A control object to control the reefer telemetry simulation
                type: object
                properties:
                  containerID:
                    type: string
                  simulation:
                    type: string
                  nb_of_records:
                    type: integer
                  product_id: 
                    type: string
            example:
              containerID: C02
              simulation: co2sensor
              nb_of_records: 25
              product_id: P02
    responses:
      202:
        description: A successful reply
        examples:
          text/plain: Simulation started!
      400:
        description: Container ID is missing
      404:
        description: Wrong simulation controller data error
    components:
      schemas:
        Control:
          title: A control object to control the reefer telemetry simulation
          type: object
          properties:
            containerID:
              type: string
            simulation:
              type: string
            nb_of_records:
              type: integer
            product_id: 
              type: string
    """
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


# It is considered bad form to return an error for '/', so let's redirect to the apidocs
@app.route('/')
def index():
    return redirect('/apidocs')

# If you have additional modules that contain your API endpoints, for instance
# using Blueprints, then ensure that you use relative imports, e.g.:
# from .mymodule import myblueprint
