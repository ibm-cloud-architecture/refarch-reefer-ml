
# python drive for mongodb: https://api.mongodb.com/python/current/index.html
from pymongo import MongoClient
from bson.objectid import ObjectId
import ssl,os
# pprint library is used to make the output look more pretty
from pprint import pprint



def readCsv(db):
    f = open('telemetries.csv','r')
    f.readline() # skip first line as it is the header
    for line in f:
        line =  f.readline()
        record = line.split(',')
        telemetry= toJson(record)
        insertOneTelemetry(db,telemetry)

def toJson(record):
    t = {}
    sensors = {}
    t["containerID"] = record[0]
    t["measurement_time"] = record[1]
    t["product_id"] = record[2]
    t["target_temperature"] = record[4]
    t["kilowatts"] = record[6]
    t["time_door_open"] = int(record[7])
    t["content_type"] = int(record[8])
    t["defrost_cycle"] = int(record[9])
    sensors["temperature"] = record[3]
    sensors["ambiant_temperature"] = record[5]
    sensors["oxygen_level"] = record[9]
    sensors["nitrogen_level"] = record[10]
    sensors["humidity_level"] = record[10]
    sensors["carbon_dioxide_level"] = record[12]
    sensors["fan_1"] = record[13]
    sensors["fan_2"] = record[14]
    sensors["fan_3"] = record[15]
    t["sensors"]= sensors
    t["latitude"] = "37.8226902168957"
    t["longitude"] = "-122.3248956640928"
    return t


def connectToMongo():
    # use the string found in the "composed" field of the connection information.
    URL=os.getenv('MONGO_DB_URL')
    print(URL)
    # connect to MongoDB
    client = MongoClient(URL,ssl=True,ssl_ca_certs='/home/mongodb.pem')
    db = client.ibmclouddb
    return db

def insertOneTelemetry(db,telemetry):
    result = db.telemetries.insert_one(telemetry)
    print(result.inserted_id)
    return result.inserted_id


def listTelemetryCollection(db):
    telemetries = db.telemetries.find()
    for t in telemetries:
        print(t)

def getTelemetryById(db,id):
    telemetry = db.telemetries.find_one({"_id": ObjectId(id)})
    return telemetry

if __name__ == "__main__":
    telemetry = { "timestamp": "2019-09-04 T15:41 Z",
            "containerID": "C100",
            "product_id": "P02",
            "sensors": {
                "temperature": 5.49647,
                "oxygen_level" : 20.4543,
                "nitrogen_level" : 79.4046,
                "carbon_dioxide_level" : 4.42579,
                "humidity_level" : 60.3148,
                "fan_1": "True",
                "fan_2" : "True",
                "fan_3" : "True",
                "ambiant_temperature": 19.8447
            },
            "target_temperature": 6.0,
            "kilowatts": 3.44686,
            "latitude": "37.8226902168957",
            "longitude": "-122.3248956640928",
            "time_door_open" : 0,
            "defrost_cycle": 6
            }
    
    db=connectToMongo()
    readCsv(db)
    # insertOneTelemetry(db,telemetry)
    listTelemetryCollection(db)
    # telem = getTelemetryById(db,'5ddc813c39f5241b4d4a5a43')
    # print(telem['sensors'])