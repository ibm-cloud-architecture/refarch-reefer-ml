package ibm.gse.kcontainer.scoring.infrastructure;

public class TelemetryEvent {

    String containerID;
    String payload;
    String timestamp;
    String type;

    public TelemetryEvent(){}

    public String getContainerID(){
        return containerID;
    }
    public void setContainerID(String containerID){
        this.containerID=containerID;
    }
    public String getPayload(){
        return payload;
    }
    public void setPayload(String payload){
        this.payload=payload;
    }
    public String getTimestamp(){
        return timestamp;
    }
    public void setTimestamp(String timestamp){
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
            "payload: " + this.payload +
            "}";
    }
}
