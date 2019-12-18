import os,sys, io
# python drive for mongodb: https://api.mongodb.com/python/current/index.html
from pymongo import MongoClient
import pandas as pd 
import json


def toJson(record):
    t = {}
    sensors = {}
    t["containerID"] = record[0]
    t["measurement_time"] = record[1]
    t["product_id"] = record[2]
    sensors["temperature"] = record[3]
    t["target_temperature"] = int(record[4])  # bson does not know about numpy.int64
    sensors["ambiant_temperature"] = record[5]
    t["kilowatts"] = record[6]
    t["time_door_open"] = int(record[7])
    t["content_type"] = int(record[8])
    t["defrost_cycle"] = int(record[9])
    sensors["oxygen_level"] = record[10]
    sensors["nitrogen_level"] = record[11]
    sensors["humidity_level"] = record[12]
    sensors["carbon_dioxide_level"] = record[13]
    sensors["fan_1"] = bool(record[14])   # bson does not know about numpy.bool
    sensors["fan_2"] = bool(record[15])
    sensors["fan_3"] = bool(record[16])
    t["sensors"]= sensors
    t["latitude"] = record[17]
    t["longitude"] = record[18]
    return t

class ReeferRepository:

    def __init__(self):
        self.URL = os.getenv('MONGO_DB_URL','mongodb://localhost:27017')
        print( self.URL)
        self.dbName = os.getenv('MONGO_DATABASE','ibmclouddb')
        self.tlsCert = os.getenv('MONGO_SSL_PEM','')
        self.dbUser = os.getenv('MONGODB_USER','ibmclouddb')
        self.dbPwd = os.getenv('MONGODB_PASSWORD','ibmclouddb')

    def connect(self):
        if not self.tlsCert:
            client = MongoClient(self.URL,username=self.dbUser,password=self.dbPwd,ssl=False)
            print('connection to mongodb ' + self.dbName)
        else:
            client = MongoClient(self.URL,username=self.dbUser,password=self.dbPwd,ssl=True,ssl_ca_certs=self.tlsCert)
            print('TLS connection to mongodb with ' + self.tlsCert)
        self.conn = client[self.dbName]
        return self.conn

    def createTelemetriesCollection(self):
        telemetry={ "timestamp": "2019-09-04 T15:31 Z",
                    "containerID": "C101",
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
                    "content_type": 1,
                    "target_temperature": 6.0,
                    "kilowatts": 3.44686,
                    "latitude": "37.8226902168957,",
                    "longitude": "-122.3248956640928",
                    "time_door_open" : 300,
                    "defrost_cycle": 6
                }
        result = self.conn.telemetries.insert_one(telemetry)



    def addReeferTelemetry(self,record):
        telemetry = toJson(record)
        result = self.conn.telemetries.insert_one(telemetry)
        print("Done uploading telemetry record -> " + str(result.inserted_id))
        
 
    def getAllReeferTelemetries(self):
        telemetries = self.conn.telemetries.find()
        return telemetries



if __name__ == '__main__':
    repo = ReeferRepository()
    conn=repo.connect()

    # repo.createTelemetriesCollection()
    for t in repo.getAllReeferTelemetries():
        print(t)

    