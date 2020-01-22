package ibm.gse.kcontainer.scoring.infrastructure;

import ibm.gse.kcontainer.scoring.domain.Telemetry;
import ibm.gse.kcontainer.scoring.domain.ContainerAnomaly;
import java.sql.Timestamp;

public class ContainerAnomalyEvent {

    String containerID;
    ContainerAnomaly payload;
    long timestamp;
    String type;

    public ContainerAnomalyEvent(){}

    public ContainerAnomalyEvent(String ContainerID, String timestamp, Telemetry payload){
        this.containerID = ContainerID;
        this.timestamp = Timestamp.valueOf(timestamp).getTime();
        this.type = "ContainerAnomaly";
        this.payload = new ContainerAnomaly(payload);
    }

    public String getContainerID(){
        return containerID;
    }
    public void setContainerID(String containerID){
        this.containerID=containerID;
    }
    public ContainerAnomaly getPayload(){
        return payload;
    }
    public void setPayload(ContainerAnomaly payload){
        this.payload=payload;
    }
    public long getTimestamp(){
        return timestamp;
    }
    public void setTimestamp(long timestamp){
        this.timestamp=timestamp;
    }
    public String getType(){
        return type;
    }
    public void setType(String type){
        this.type=type;
    }
    public String toString(){
        return "{" + 
            "containerID: " + this.containerID + ", " +
            "timestamp: " + this.timestamp + ", " +
            "type: " + this.type + ", " +
            "payload: " + this.payload.toString() +
            "}";
    }
}
