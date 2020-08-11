from confluent_kafka import Producer 
import json, datetime
import userapp.infrastructure.EventBackboneConfiguration as EventBackboneConfiguration

class MetricsEventsProducer:

    def __init__(self):
        self.prepareProducer("ReeferTelemetryProducers")
        
    def prepareProducer(self,groupID):
        options ={
                'bootstrap.servers':  EventBackboneConfiguration.getBrokerEndPoints(),
                'group.id': groupID,
        }
        if (EventBackboneConfiguration.isSecured()):
            options['security.protocol'] = 'SASL_SSL'
            # If we are connecting to ES on IBM Cloud, the SASL mechanism is plain
            if (EventBackboneConfiguration.getKafkaUser() == 'token'):
                options['sasl.mechanisms'] = 'PLAIN'
            # If we are connecting to ES on OCP, the SASL mechanism is scram-sha-512
            else:
                options['sasl.mechanisms'] = 'SCRAM-SHA-512'
            options['sasl.username'] = EventBackboneConfiguration.getKafkaUser()
            options['sasl.password'] = EventBackboneConfiguration.getKafkaPassword()
        if (EventBackboneConfiguration.isEncrypted()):
            options['ssl.ca.location'] = EventBackboneConfiguration.getKafkaCertificate()
        print("Kafka options are:")
        print(options)
        self.producer = Producer(options)


    def delivery_report(self,err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print( str(datetime.datetime.today()) + ' - Message delivery failed: {}'.format(err))
        else:
            print(str(datetime.datetime.today()) + ' - Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def publishEvent(self, eventToSend, keyName):
        dataStr = json.dumps(eventToSend)
        print(dataStr)
        self.producer.produce(EventBackboneConfiguration.getTelemetryTopicName(),
                            key=eventToSend[keyName],
                            value=dataStr.encode('utf-8'), 
                            callback=self.delivery_report)
        self.producer.flush()

    def close(self):
        self.producer.close()