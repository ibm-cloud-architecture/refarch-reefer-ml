from flask import Flask, request, jsonify, abort
import os, time, sys
from datetime import datetime
from domain.predictservice import PredictService

VERSION = "Reefer Container Predictive Scoring v0.0.2"
# used by gunicorn
application = Flask(__name__)
predictService = PredictService()
header="""Temperature(celsius), Target_Temperature(celsius), Power, PowerConsumption, ContentType, O2, CO2, Time_Door_Open, Maintenance_Required, Defrost_Cycle"""


@application.route("/")
def hello():
    return VERSION


@application.route("/predict", methods = ['POST'])
def predictContainerTelemetry():
    metricValue = transformToCSV(request.json)
    metric = header+"\n"+metricValue
    print(metric)
    score=str(predictService.predict(metric))
    print(score)
    return score
   

def transformToCSV(metricJson):
    return str(metricJson["temperature"]) + "," \
        + str(metricJson["target_temp"]) + "," \
        + str(metricJson["power"]) + "," \
        + str(metricJson["accumulated_power"]) + "," \
        + str(metricJson["content_type"]) + "," \
        + str(metricJson["o2"]) + "," \
        + str(metricJson["co2"]) + "," \
        + str(metricJson["time_door_open"]) + ",0," \
        + str(metricJson["defrost_level"])




if __name__ == "__main__":
    print(VERSION)
    application.run()
 