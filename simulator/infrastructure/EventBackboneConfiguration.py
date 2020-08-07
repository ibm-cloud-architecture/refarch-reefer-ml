import os

KAFKA_BROKERS = os.getenv('KAFKA_BROKERS','localhost:9092')
KAFKA_PASSWORD = os.getenv('KAFKA_PASSWORD','')
KAFKA_USER = os.getenv('KAFKA_USER','')
KAFKA_CERT = os.getenv('KAFKA_CERT','')

def getBrokerEndPoints():
    return KAFKA_BROKERS

def getKafkaPassword():
    return KAFKA_PASSWORD

def getKafkaUser():
    return KAFKA_USER

def isSecured():
    return KAFKA_APIKEY != ''

def isEncrypted():
    #return KAFKA_CERT != ''
    return os.path.isfile(KAFKA_CERT)

def getKafkaCertificate():
    return KAFKA_CERT

def getTelemetryTopicName():
    return os.getenv("MP_MESSAGING_INCOMING_REEFER_TELEMETRY_TOPIC","reefer-telemetry")
