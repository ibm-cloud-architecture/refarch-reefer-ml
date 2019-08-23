from flask import Flask, request, jsonify, abort
import os, time, datetime
from KcProducer import KafkaProducer 

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

application = Flask(__name__)

kp = KafkaProducer(KAFKA_ENV,KAFKA_BROKERS,KAFKA_APIKEY)
kp.prepareProducer("ReeferMetricsSimulator")

@application.route("/")
def hello():
    print(KAFKA_BROKERS)
    return "Reefer Container simulator v01"
    
@application.route("/control", methods = ['POST'])
def runSimulator():
    print(request.json)
    if not 'containerID' in request.json:
        abort(400) 
    control = request.json
    
    evt = {"containerID": control["containerID"],"timestamp": int(datetime.datetime.today()),"type":"ContainerMetric","payload": order}
    kp.publishEvent('containerMetrics',evt,"containerID")
    return jsonify(evt)

def produceMetricEvents(cid="101", nb_records= MAX_RECORDS, tgood=4.4):
    print("Producing metrics events")
    print ("Done!")
    
if __name__ == "__main__":
    application.run(debug=True)
    
