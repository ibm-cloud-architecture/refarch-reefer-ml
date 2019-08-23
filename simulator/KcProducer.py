import json
from confluent_kafka import KafkaError, Producer

class KafkaProducer:

    def __init__(self,kafka_env = 'LOCAL',kafka_brokers = "",kafka_apikey = ""):
        self.kafka_env = kafka_env
        self.kafka_brokers = kafka_brokers
        self.kafka_apikey = kafka_apikey

    def prepareProducer(self,groupID = "pythonorderproducers"):
        options ={
                'bootstrap.servers':  self.kafka_brokers,
                'group.id': groupID
        }
        if (self.kafka_env != 'LOCAL'):
            options['security.protocol'] = 'sasl_ssl'
            options['sasl.mechanisms'] = 'PLAIN'
            options['ssl.ca.location'] = '/etc/pki/tls/cert.pem'
            options['sasl.username'] = 'token'
            options['sasl.password'] = self.kafka_apikey
        print(options)
        self.producer = Producer(options)

    def delivery_report(self,err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def publishEvent(self, topicName, eventToSend, keyName):
        dataStr = json.dumps(eventToSend)
        self.producer.produce(topicName,key=eventToSend[keyName],value=dataStr.encode('utf-8'), callback=self.delivery_report)
        self.producer.flush()