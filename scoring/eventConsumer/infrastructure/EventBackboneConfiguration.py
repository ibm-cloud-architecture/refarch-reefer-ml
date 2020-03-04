import os

KAFKA_BROKERS = os.getenv('KAFKA_BROKERS','localhost:9092')
KAFKA_APIKEY = os.getenv('KAFKA_APIKEY','')
KAFKA_CERT = os.getenv('KAFKA_CERT','')

def getBrokerEndPoints():
    return KAFKA_BROKERS

def getEndPointAPIKey():
    return KAFKA_APIKEY

def hasAPIKey():
    return KAFKA_APIKEY != ''

def isEncrypted():
    return KAFKA_CERT != ""

def getKafkaCertificate():
    return KAFKA_CERT

def getTelemetryTopicName():
    return os.getenv("TELEMETRY_TOPIC","reefer-telemetry")

def getContainerTopicName():
    return os.getenv("CONTAINER_TOPIC","containers")
