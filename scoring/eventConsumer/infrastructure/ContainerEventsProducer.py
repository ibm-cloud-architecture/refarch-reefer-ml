from confluent_kafka import Producer 
import json
import infrastructure.EventBackboneConfiguration as EventBackboneConfiguration

class ContainerEventsProducer:

    def __init__(self):
        self.currentRuntime = EventBackboneConfiguration.getCurrentRuntimeEnvironment()
        self.brokers = EventBackboneConfiguration.getBrokerEndPoints()
        self.apikey = EventBackboneConfiguration.getEndPointAPIKey()
        self.topic_name = "containers"
        self.prepareProducer("pythonproducers")
        
    def prepareProducer(self,groupID = "pythonproducers"):
        options ={
                'bootstrap.servers':  self.brokers,
                'group.id': groupID
        }
        # We need this test as local kafka does not expect SSL protocol.
        if (self.currentRuntime != 'LOCAL'):
            options['security.protocol'] = 'SASL_SSL'
            options['sasl.mechanisms'] = 'PLAIN'
            options['sasl.username'] = 'token'
            options['sasl.password'] = self.apikey
        if (self.currentRuntime == 'ICP'):
            options['ssl.ca.location'] = 'es-cert.pem'
        print(options)
        self.producer = Producer(options)

    def delivery_report(self,err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def publishEvent(self, eventToSend, keyName):
        dataStr = json.dumps(eventToSend)
        self.producer.produce("containers",
                            key=eventToSend[keyName],
                            value=dataStr.encode('utf-8'), 
                            callback=self.delivery_report)
        self.producer.flush()

    def close(self):
        self.producer.close()