import os, sys

try:
    KAFKA_BROKERS = os.environ['KAFKA_BROKERS']
except KeyError:
    print("The KAFKA_BROKERS environment variable needs to be set.")
    exit

try:
    KAFKA_APIKEY = os.environ['KAFKA_APIKEY']
except KeyError:
    print("The KAFKA_APIKEY environment variable not set... assume local deployment")
    KAFKA_APIKEY = ""

try:
    KAFKA_ENV = os.environ['KAFKA_ENV']
except KeyError:
    KAFKA_ENV = 'LOCAL'


def getBrokerEndPoints():
    return KAFKA_BROKERS

def getEndPointAPIKey():
    return KAFKA_APIKEY

def getCurrentRuntimeEnvironment():
    return KAFKA_ENV