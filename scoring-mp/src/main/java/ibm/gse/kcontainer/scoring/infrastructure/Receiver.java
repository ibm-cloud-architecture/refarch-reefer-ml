package ibm.gse.kcontainer.scoring.infrastructure;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import org.eclipse.microprofile.reactive.messaging.Incoming;
import org.eclipse.microprofile.reactive.messaging.Outgoing;
import org.eclipse.microprofile.reactive.messaging.Message;
import org.eclipse.microprofile.reactive.messaging.Acknowledgment;
import org.eclipse.microprofile.reactive.streams.PublisherBuilder;
import org.eclipse.microprofile.reactive.streams.ReactiveStreams;
// import org.eclipse.microprofile.reactive.streams.operators.ReactiveStreams;

import ibm.gse.kcontainer.scoring.domain.Telemetry;

import javax.enterprise.context.ApplicationScoped;
import java.util.Arrays;
//import io.smallrye.reactive.messaging.kafka.KafkaMessage;
import java.util.Random;

@ApplicationScoped
public class Receiver {

    ScoringClient scoringClient = new ScoringClient();

    @Incoming("testReactive")
    @Outgoing("testOutput")
    @Acknowledgment(Acknowledgment.Strategy.MANUAL)
    // public KafkaMessage<Integer, String> processTelemetry(String input) {
    // public String processTelemetry(String input) {
    public PublisherBuilder<Message<String>> processTelemetry(Message<String> message) {
        
        // Get the message as String
        String input = message.getPayload();

        int number = new Random().nextInt(10);
        
        System.out.println("**********************");
        System.out.println("**********************");
        System.out.println("Number is: " + number);

        if (number % 2 == 0){
            System.out.println("**********************");
            System.out.println("No processing at all");
            message.ack(); // All processing of this message is done, ack it now
            return ReactiveStreams.empty();
        }
        else{
            System.out.println("**********************");
            System.out.println("**********************");
            System.out.println("Received message: " + input);

            System.out.println("**********************");
            System.out.println("**********************");
            System.out.println("Transforming message into a TelemetryEvent Java Object");
            Gson g = new Gson();
            TelemetryEvent te = g.fromJson(input, TelemetryEvent.class);
            System.out.println("TelemetryEvent object: " + te.toString());

            System.out.println("**********************");
            System.out.println("**********************");
            System.out.println("Getting the Telemetry as Java Object");
            Telemetry t = new Telemetry(te.getPayload());
            System.out.println("Telemetry object: " + t.toString());

            System.out.println("**********************");
            System.out.println("**********************");
            System.out.println("Creating the ContainerAnomalyEvent Java object");
            ContainerAnomalyEvent cae = new ContainerAnomalyEvent(te.getContainerID(), te.getTimestamp(), t);
            System.out.println("ContainerAnomalyEvent object: " + cae.toString());

            System.out.println("**********************");
            System.out.println("**********************");
            System.out.println("Produce Output");

            // This message will be sent on, create a new message which acknowledges the incoming message when it is acked
            return ReactiveStreams.of(Message.of(cae.toString(), () -> message.ack()));
            
            // return cae.toString();
            // return KafkaMessage.of("testOutput",new Integer(1111), "This is a message");
        }
    }

    // @Incoming("testReactive")
    // public void processTelemetry(String input) {
        
    //         System.out.println("**********************");
    //         System.out.println("**********************");
    //         System.out.println("Received message: " + input);

    //         System.out.println("**********************");
    //         System.out.println("**********************");
    //         System.out.println("Transforming message into a TelemetryEvent Java Object");
    //         Gson g = new Gson();
    //         TelemetryEvent te = g.fromJson(input, TelemetryEvent.class);
    //         System.out.println("TelemetryEvent object: " + te.toString());

    //         System.out.println("**********************");
    //         System.out.println("**********************");
    //         System.out.println("Getting the Telemetry as Java Object");
    //         Telemetry t = new Telemetry(te.getPayload());
    //         System.out.println("Telemetry object: " + t.toString());

    //         System.out.println("**********************");
    //         System.out.println("**********************");
    //         System.out.println("CALLING");
    //         ScoringResult scoringResult = scoringClient.callAnomalyScoring(t);
    //         ScoringPrediction[] predictions = scoringResult.getPredictions();
    //         System.out.println("Number of predictions: " + predictions.length);

    //         // iterating over an array 
    //         for (int i = 0; i < predictions.length; i++) { 
    //             // accessing each element of array 
    //             System.out.println("Iteration: " + i);
    //             ScoringPrediction x = predictions[i]; 
    //             String[] fields = x.getFields();
    //             Object[][] values = x.getValues();
    //             System.out.println("Length of fields: " + fields.length);
    //         } 

    //         // System.out.println("**********************");
    //         // System.out.println("**********************");
    //         // System.out.println("Creating the ContainerAnomalyEvent Java object");
    //         // ContainerAnomalyEvent cae = new ContainerAnomalyEvent(te.getContainerID(), te.getTimestamp(), t);
    //         // System.out.println("ContainerAnomalyEvent object: " + cae.toString());

    //         // System.out.println("**********************");
    //         // System.out.println("**********************");
    //         // System.out.println("Produce Output");
    // }

    // @Outgoing("testOutput")
    // public Message<String> produce(JsonObject json){
    //     return Message.of(json.toString());
    // }

    public String retrieve(String id) {
        return "test";
    }

}
