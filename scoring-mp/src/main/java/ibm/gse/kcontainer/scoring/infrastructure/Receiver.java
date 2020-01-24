package ibm.gse.kcontainer.scoring.infrastructure;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import org.eclipse.microprofile.config.inject.ConfigProperty;
import org.eclipse.microprofile.reactive.messaging.Incoming;
import org.eclipse.microprofile.reactive.messaging.Outgoing;
import org.eclipse.microprofile.reactive.messaging.Message;
import org.eclipse.microprofile.reactive.messaging.Acknowledgment;
import org.eclipse.microprofile.reactive.streams.operators.PublisherBuilder;
import org.eclipse.microprofile.reactive.streams.operators.ReactiveStreams;

import ibm.gse.kcontainer.scoring.domain.Telemetry;

import javax.enterprise.context.ApplicationScoped;
import java.util.Arrays;
import java.util.Random;
import javax.inject.Inject;

@ApplicationScoped
public class Receiver {

    @Inject ScoringClient scoringClient;

    @Inject
    @ConfigProperty(name = "mockup")
    private String mockup;

    @Incoming("reeferTelemetry")
    @Outgoing("containers")
    @Acknowledgment(Acknowledgment.Strategy.MANUAL)
    public PublisherBuilder<Message<String>> processTelemetry(Message<String> message) {

        // Get the message as String
        String input = message.getPayload();
        System.out.println("Received message: " + input);

        Gson g = new Gson();
        // Parsing the message into a TelemetryEvent Java Object
        TelemetryEvent te = g.fromJson(input, TelemetryEvent.class);
        // Getting the Telemetry out of the event.
        Telemetry t = new Telemetry(te.getPayload());

        // Calling the Anomaly Scoring service
        ScoringResult scoringResult = scoringClient.callAnomalyScoring(t);
        // Getting the Scoring Prediction Results
        ScoringPredictionValues result = scoringResult.getScoringPredictionValues();
        System.out.println("This is the prediction: " + result.getPrediction());
        System.out.println("This is the probability: " + "[" + result.getMetrics()[0] + "," + result.getMetrics()[1] + "]");

        Boolean anomaly = false;

        if (mockup.equals("yes")){
            // Mockup
            int number = new Random().nextInt(10);
            System.out.println("Number: " + number);
            if (number > 6) anomaly = true;
        }
        else{
            anomaly = result.getPrediction().equalsIgnoreCase("Issue");
        }

        if (!anomaly){
            System.out.println("No container anomaly");
            message.ack(); // All processing of this message is done, ack it now
            return ReactiveStreams.empty();
        }
        else{
            System.out.println("A container anomaly has been predicted. Therefore, sending a ContainerAnomaly Event to the appropriate topic");
            ContainerAnomalyEvent cae = new ContainerAnomalyEvent(te.getContainerID(), te.getTimestamp(), t);
            System.out.println("ContainerAnomalyEvent object sent: " + cae.toString());

            // This message will be sent on, create a new message which acknowledges the incoming message when it is acked
            return ReactiveStreams.of(Message.of(cae.toString(), () -> message.ack()));
        }
    }

    public String retrieve(String id) {
        return "test";
    }

}
