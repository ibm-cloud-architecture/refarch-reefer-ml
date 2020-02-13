from flask import Flask, redirect, request, jsonify, abort
from flasgger import Swagger
from server import app
from server.routes.prometheus import track_requests
import os, time, sys
from datetime import datetime
from userapp.domain.predictservice import PredictService

predictService = PredictService()
# The python-flask stack includes the flask extension flasgger, which will build
# and publish your swagger ui and specification at the /apidocs url. Here we set up
# the basic swagger attributes, which you should modify to match you application.
# See: https://github.com/rochacbruno-archive/flasgger
swagger_template = {
  "swagger": "2.0",
  "info": {
    "title": "Example API for python-flask stack",
    "description": "API for helloworld, plus health/monitoring",
    "contact": {
      "responsibleOrganization": "IBM",
      "responsibleDeveloper": "Henry Nash",
      "email": "henry.nash@uk.ibm.com",
      "url": "https://appsody.dev",
    },
    "version": "0.2"
  },
  "schemes": [
    "http"
  ],
}

swagger = Swagger(app, template=swagger_template)

# The python-flask stack includes the prometheus metrics engine. You can ensure your endpoints
# are included in these metrics by enclosing them in the @track_requests wrapper.
@app.route('/hello')
@track_requests
def HelloWorld():
    # To include an endpoint in the swagger ui and specification, we include a docstring that
    # defines the attributes of this endpoint.
    """A hello message
    Example endpoint returning a hello message
    ---
    responses:
      200:
        description: A successful reply
        examples:
          text/plain: Hello from Appsody!
    """
    return 'Hello from Appsody!'

# This route is just to test and debug.
heroes = [{'name' : 'Batman'}, {'name' : 'Superman'}]
@app.route('/superHeros', methods = ['GET', 'POST'])
@track_requests
def SuperHero():
    """A test message
    Example endpoint returning a Test message
    ---
    responses:
      200:
        description: A good reply
        examples:
          text/plain: Test from Appsody!
    """
    content = request.get_json()
    heroes.append(content)
    return jsonify(heroes)

# It is considered bad form to return an error for '/', so let's redirect to the apidocs
@app.route('/')
def index():
    return redirect('/apidocs')

sample = {
    "temperature" : 12,
    "target_temperature" : 13,
    "ambiant_temperature" : 14,
    "oxygen_level" : 15,
    "carbon_dioxide_level" : 16,
    "humidity_level" : 17,
    "nitrogen_level" : 18,
    "vent_1" : 19,
    "vent_2" : 21,
    "vent_3" : 31,
    "kilowatts" : 41,
    "content_type" : 51,
    "time_door_open" : 61,
    "defrost_cycle": 71
 }
header = "temperature, target_temperature, ambiant_temperature, oxygen_level, carbon_dioxide_level, humidity_level, nitrogen_level, vent_1, vent_2, vent_3, kilowatts, content_type, time_door_open, defrost_cycle"

@app.route("/predict", methods = ['POST'])
def predictContainerTelemetry():
    """Post Score
    Endpoint returning score from predictService
    ---
    consumes:
        - application-json
    parameters:
      - in: body
        name: telemetry
        description: Incoming telemetry data from a single TelemetryEvent
        required: true
        example:
            temperature: 12
            target_temperature: 13
            ambiant_temperature: 14
            oxygen_level: 15
            carbon_dioxide_level: 16
            humidity_level: 17
            nitrogen_level: 18
            vent_1: 19
            vent_2: 21
            vent_3: 31
            kilowatts: 41
            content_type: 51
            time_door_open: 61
            defrost_cycle: 71
    responses:
      200:
        description: Scoring result from the Pickle model, determining whether the telemetry data should generate a ContainerAnomalyEvent. 0 if no maintenance is needed, 1 otherwise.
        examples:
          application/json: [0]
    """
    telemetry_json = request.get_json(force=True)
    metricValue = transformToCSV(telemetry_json)
    metric = header + "\n" + metricValue
    print("Predict with this parameter " + metric)
    score=str(predictService.predict(metric))
    print("return prediction:" + score)
    return jsonify(score)

def transformToCSV(metricJson):
    return str(metricJson["temperature"]) + "," \
        + str(metricJson["target_temperature"]) + "," \
        + str(metricJson["ambiant_temperature"]) + "," \
        + str(metricJson["oxygen_level"]) + "," \
        + str(metricJson["carbon_dioxide_level"]) + "," \
        + str(metricJson["humidity_level"]) + "," \
        + str(metricJson["nitrogen_level"]) + "," \
        + str(metricJson["vent_1"]) + "," \
        + str(metricJson["vent_2"]) + "," \
        + str(metricJson["vent_3"]) + "," \
        + str(metricJson["kilowatts"]) + "," \
        + str(metricJson["content_type"]) + "," \
        + str(metricJson["time_door_open"]) + "," \
        + str(metricJson["defrost_cycle"])


# If you have additional modules that contain your API endpoints, for instance
# using Blueprints, then ensure that you use relative imports, e.g.:
# from .mymodule import myblueprint
