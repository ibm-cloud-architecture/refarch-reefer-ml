from flask import Flask, request, jsonify, abort
import os, time
from datetime import datetime
from KcProducer import KafkaProducer 
from reefer_simulator import ReeferSimulator

try:
    KAFKA_BROKERS = os.environ['KAFKA_BROKERS']
except KeyError:
    KAFKA_BROKERS = "localhost:9092"

try:
    KAFKA_APIKEY = os.environ['KAFKA_APIKEY']
except KeyError:
    print("The KAFKA_APIKEY environment variable not set... assume local deployment")

try:
    KAFKA_ENV = os.environ['KAFKA_ENV']
except KeyError:
    KAFKA_ENV='LOCAL'

POWEROFF_SIMUL="poweroff"
CO2_SIMUL="co2sensor"

application = Flask(__name__)

kp = KafkaProducer(KAFKA_ENV,KAFKA_BROKERS,KAFKA_APIKEY)
kp.prepareProducer("ReeferMetricsSimulator")

@application.route("/")
def hello():
    print(KAFKA_BROKERS)
    return "Reefer Container simulator v0.0.2"
    
@application.route("/control", methods = ['POST'])
def runSimulator():
    print(request.json)
    if not 'containerID' in request.json:
        abort(400) 
    control = request.json
    simulator = ReeferSimulator()
    if control["simulation"] == POWEROFF_SIMUL:
        metrics=simulator.generatePowerOffTuples(control["containerID"],int(control["nb_of_records"]),float(control["good_temperature"]))
    elif  control["simulation"]  == CO2_SIMUL:
        metrics=simulator.generateCo2Tuples(control["containerID"],int(control["nb_of_records"]),float(control["good_temperature"]))
    else:
        return "Wrong simulation controller data"
    
    for metric in metrics:
        ts=time.strptime(metric[0],"%Y-%m-%d T%H:%M Z")
        evt = {"containerID": control["containerID"],
                "timestamp": int(time.mktime(ts)),
                "type":"ContainerMetric",
                "payload": str(metric)}
        kp.publishEvent('containerMetrics',evt,"containerID")
    return "Simulation started"
    

if __name__ == "__main__":
    application.run(debug=True)
    
