from flask import Flask, request, jsonify, abort
import os, time, sys
from datetime import datetime
from domain.predictservice import PredictService

VERSION = "Reefer Container Predictive Scoring v0.0.2"
# used by gunicorn
application = Flask(__name__)
predictService = PredictService()
header="""temperature,target_temperature,ambiant_temperature,oxygen_level,carbon_dioxide_level,humidity_level,nitrogen_level,vent_1,vent_2,vent_3,kilowatts,content_type,time_door_open,defrost_cycle"""


@application.route("/")
def hello():
    return VERSION


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




if __name__ == "__main__":
    print(VERSION)
    application.run()
