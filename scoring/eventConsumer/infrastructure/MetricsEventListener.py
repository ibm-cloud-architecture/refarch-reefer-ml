import json
from confluent_kafka import Consumer, KafkaError
import infrastructure.EventBackboneConfiguration as EventBackboneConfiguration

class MetricsEventListener:

    def __init__(self):
        self.currentRuntime = EventBackboneConfiguration.getCurrentRuntimeEnvironment()
        self.brokers = EventBackboneConfiguration.getBrokerEndPoints()
        self.apikey = EventBackboneConfiguration.getEndPointAPIKey()
        self.topic_name = "containerMetrics"
        self.kafka_auto_commit = True
        self.prepareConsumer()

    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    def prepareConsumer(self, groupID = "reefermetricsconsumer"):
        options ={
                'bootstrap.servers':  self.brokers,
                'group.id': groupID,
                 'auto.offset.reset': 'earliest',
                'enable.auto.commit': self.kafka_auto_commit,
        }
        if (self.currentRuntime != 'LOCAL' and self.currentRuntime != 'MINIKUBE'):
            options['security.protocol'] = 'SASL_SSL'
            options['sasl.mechanisms'] = 'PLAIN'
            options['sasl.username'] = 'token'
            options['sasl.password'] = self.apikey
        print(options)
        self.consumer = Consumer(options)
        self.consumer.subscribe([self.topic_name])
    
    def traceResponse(self, msg):
        msgStr = msg.value().decode('utf-8')
        print('@@@ pollNextEvent {} partition: [{}] at offset {} with key {}:\n\tvalue: {}'
                    .format(msg.topic(), msg.partition(), msg.offset(), str(msg.key()), msgStr ))
        return msgStr

    def processEvents(self, callback):
        gotIt = False
        anEvent = {}
        while not gotIt:
            msg = self.consumer.poll(timeout=10.0)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                if ("PARTITION_EOF" in msg.error()):
                    gotIt= True
                continue
            msgStr = self.traceResponse(msg)
            anEvent = json.loads(msgStr)
            gotIt = callback(anEvent)
    
    def close(self):
        self.consumer.close()