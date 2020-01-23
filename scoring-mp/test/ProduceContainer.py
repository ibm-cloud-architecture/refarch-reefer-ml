import os, time, sys
from KcProducer import KafkaProducer

print(" @@@ Executing script: ProduceContainer.py")

####################### READ ENV VARIABLES #######################
# Try to read the Kafka broker from the environment variables
try:
    KAFKA_BROKERS = os.environ['KAFKA_BROKERS']
except KeyError:
    print("[ERROR] - The KAFKA_BROKERS environment variable needs to be set.")
    exit(1)

# Try to read the Kafka API key from the environment variables
try:
    KAFKA_APIKEY = os.environ['KAFKA_APIKEY']
except KeyError:
    print("The KAFKA_APIKEY environment variable not set... assume local deployment")

# Try to read the Kafka environment from the environment variables
try:
    KAFKA_ENV = os.environ['KAFKA_ENV']
except KeyError:
    KAFKA_ENV='LOCAL'

####################### VARIABLES #######################
ID = "c01"
TOPIC_NAME="test"

####################### FUNCTIONS #######################
# Create a default container
def createContainer(id):
    print('Creating container...', end ='')
    
    # data = {"containerID": id, 
    #     "type": "Reefer", 
    #     "status": "Empty",
    #     "latitude": 37.80,
    #     "longitude":  -122.25,
    #     "capacity": 110, 
    #     "brand": "itg-brand"}
    # containerEvent = {"containerID": id,"timestamp": int(time.time()),"type":"ContainerAdded","payload": data}

    # containerEvent = {"containerID": "1111",  "temperature": 12.0,
    # "target_temperature": 12.0,
    # "ambiant_temperature": 12.0,
    # "kilowatts": 12.0,
    # "time_door_open": 12.0,
    # "content_type": 11,
    # "defrost_cycle": 11,
    # "oxygen_level": 12.0,
    # "nitrogen_level": 12.0,
    # "humidity_level": 12.0,
    # "target_humidity_level": 12.0,
    # "carbon_dioxide_level": 12.0,
    # "fan_1": "true",
    # "fan_2": "true",
    # "fan_3": "true"}
    containerEvent = {
  "containerID": "1111",
  "payload": "('1111', '2020-01-15 17:59:45', 'P05', 5.02702153, 5., 20.52035697, 2.62176459, 0, 1, 5, 21.56977522, 75.97754859, 39.85714797, 4.74727473, True, True, True, '37.8226902168957', '-122.324895', 0)",
  "timestamp": "2020-01-15 17:59:45",
  "type": "ReeferTelemetries"
    }
    print("DONE")
    return containerEvent

# Parse arguments to get the Container ID
def parseArguments():
    global TOPIC_NAME, ID
    print("The arguments for the script are: " , str(sys.argv))
    if len(sys.argv) == 3:
        ID = sys.argv[1]
        TOPIC_NAME = sys.argv[2]
    else:
        print("[ERROR] - The ProduceContainer.py script expects two arguments: The container ID and the topic to send the container event to.")
        exit(1)

####################### MAIN #######################
if __name__ == '__main__':
    parseArguments()
    evt = createContainer(ID)
    print("Container event to be published:")
    print(evt)
    kp = KafkaProducer(KAFKA_ENV,KAFKA_BROKERS,KAFKA_APIKEY)
    kp.prepareProducer("ProduceContainerPython")
    kp.publishEvent(TOPIC_NAME,evt,"containerID")
