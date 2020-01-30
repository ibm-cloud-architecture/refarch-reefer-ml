from flask import Flask, redirect, request, jsonify, abort
from flasgger import Swagger
from server import app
from server.routes.prometheus import track_requests
import os, time, sys
from datetime import datetime
from userapp.domain.predictservice import PredictService

application = Flask(__name__)
# predictService = PredictService()
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

@app.route('/test')
@track_requests
def TestWorld():
    # To include an endpoint in the swagger ui and specification, we include a docstring that
    # defines the attributes of this endpoint.
    """A test message
    Example endpoint returning a Test message
    ---
    responses:
      200:
        description: A good reply
        examples:
          text/plain: Test from Appsody!
    """
    return 'Trying some stuff out'

# It is considered bad form to return an error for '/', so let's redirect to the apidocs
@app.route('/')
def index():
    return redirect('/apidocs')

@application.route("/predict", methods = ['POST'])
def predictContainerTelemetry():
    metricValue = transformToCSV(request.json)
    metric = header+"\n"+metricValue
    print("Predict with this parameter " + metric)
    score=str(predictService.predict(metric))
    print("return prediction:" + score)
    return score


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
