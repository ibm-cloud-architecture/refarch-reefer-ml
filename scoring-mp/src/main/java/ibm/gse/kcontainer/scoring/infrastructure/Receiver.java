package ibm.gse.kcontainer.scoring.infrastructure;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import org.eclipse.microprofile.reactive.messaging.Incoming;
import org.eclipse.microprofile.reactive.messaging.Outgoing;
import org.eclipse.microprofile.reactive.messaging.Message;
import ibm.gse.kcontainer.scoring.domain.Telemetry;

import javax.enterprise.context.ApplicationScoped;

@ApplicationScoped
public class Receiver {

    @Incoming("testReactive")
    @Outgoing("testOutput")
    public String consume(String json_input) {
        System.out.println("Receiving " + json_input);
        System.out.println("Transforming message into a Telemetry Java Object");
        Gson g = new Gson();
        Telemetry t = g.fromJson(json_input, Telemetry.class);
        System.out.println("Transformed");
        System.out.println("Printing it out now:");
        System.out.println(t.toString());
        System.out.println("DOING JsonObject now:");
        JsonObject jsonObject = new JsonParser().parse(json_input).getAsJsonObject();
        System.out.println(jsonObject.get("containerID").toString());
        System.out.println("Producing message");
        return jsonObject.toString();
    }

    // @Outgoing("testOutput")
    // public Message<String> produce(JsonObject json){
    //     return Message.of(json.toString());
    // }

    public String retrieve(String id) {
        return "test";
    }

}
