package ibm.gse.kcontainer.scoring.domain;

public class ContainerAnomaly {
    double temperature;
    double target_temperature; 
    double ambiant_temperature; 
    double kilowatts; 
    double time_door_open;
    int content_type; 
    int defrost_cycle;
    double oxygen_level; 
    double nitrogen_level; 
    double humidity_level;
    double carbon_dioxide_level; 
    boolean fan_1; 
    boolean fan_2; 
    boolean fan_3;
    double latitude;
    double longitude;

    public ContainerAnomaly(){
        
    }

    public ContainerAnomaly(Telemetry t){
        this.temperature = t.getTemperature();
        this.target_temperature = t.getTarget_temperature();
        this.ambiant_temperature = t.getAmbiant_temperature();
        this.kilowatts = t.getKilowatts();
        this.time_door_open = t.getTime_door_open();
        this.content_type = t.getContent_type();
        this.defrost_cycle = t.getDefrost_cycle();
        this.oxygen_level = t.getOxygen_level();
        this.nitrogen_level = t.getNitrogen_level();
        this.humidity_level = t.getHumidity_level();
        this.carbon_dioxide_level = t.getCarbon_dioxide_level();
        this.fan_1 = t.isFan_1();
        this.fan_2 = t.isFan_2();
        this.fan_3 = t.isFan_3();
        this.latitude = t.getLatitude();
        this.longitude = t.getLongitude();
    }

    public double getTemperature() {
        return temperature;
    }

    public void setTemperature(double temperature) {
        this.temperature = temperature;
    }

    public double getTarget_temperature() {
        return target_temperature;
    }

    public void setTarget_temperature(double target_temperature) {
        this.target_temperature = target_temperature;
    }

    public double getAmbiant_temperature() {
        return ambiant_temperature;
    }

    public void setAmbiant_temperature(double ambiant_temperature) {
        this.ambiant_temperature = ambiant_temperature;
    }

    public double getKilowatts() {
        return kilowatts;
    }

    public void setKilowatts(double kilowatts) {
        this.kilowatts = kilowatts;
    }

    public double getTime_door_open() {
        return time_door_open;
    }

    public void setTime_door_open(double time_door_open) {
        this.time_door_open = time_door_open;
    }

    public int getContent_type() {
        return content_type;
    }

    public void setContent_type(int content_type) {
        this.content_type = content_type;
    }

    public int getDefrost_cycle() {
        return defrost_cycle;
    }

    public void setDefrost_cycle(int defrost_cycle) {
        this.defrost_cycle = defrost_cycle;
    }

    public double getOxygen_level() {
        return oxygen_level;
    }

    public void setOxygen_level(double oxygen_level) {
        this.oxygen_level = oxygen_level;
    }

    public double getNitrogen_level() {
        return nitrogen_level;
    }

    public void setNitrogen_level(double nitrogen_level) {
        this.nitrogen_level = nitrogen_level;
    }

    public double getHumidity_level() {
        return humidity_level;
    }

    public void setHumidity_level(double humidity_level) {
        this.humidity_level = humidity_level;
    }

    public double getCarbon_dioxide_level() {
        return carbon_dioxide_level;
    }

    public void setCarbon_dioxide_level(double carbon_dioxide_level) {
        this.carbon_dioxide_level = carbon_dioxide_level;
    }

    public boolean isFan_1() {
        return fan_1;
    }

    public void setFan_1(boolean fan_1) {
        this.fan_1 = fan_1;
    }

    public boolean isFan_2() {
        return fan_2;
    }

    public void setFan_2(boolean fan_2) {
        this.fan_2 = fan_2;
    }

    public boolean isFan_3() {
        return fan_3;
    }

    public void setFan_3(boolean fan_3) {
        this.fan_3 = fan_3;
    }

    public double getLatitude(){
        return this.latitude;
    }

    public void setLatitude(double latitude){
        this.latitude=latitude;
    }

    public double getLongitude(){
        return this.longitude;
    }

    public void setLongitude(double longitude){
        this.longitude=longitude;
    }

    public String toString(){
        return "{" +
        "temperature: " + this.temperature + ", " +
        "target_temperature: " + this.target_temperature + ", " +
        "ambiant_temperature: " + this.ambiant_temperature + ", " +
        "kilowatts: " + this.kilowatts + ", " +
        "time_door_open: " + this.time_door_open + ", " +
        "content_type: " + this.content_type + ", " +
        "defrost_cycle: " + this.defrost_cycle + ", " +
        "oxygen_level: " + this.oxygen_level + ", " +
        "nitrogen_level: " + this.nitrogen_level + ", " +
        "humidity_level: " + this.humidity_level + ", " +
        "carbon_dioxide_level: " + this.carbon_dioxide_level + ", " +
        "fan_1: " + this.fan_1 + ", " +
        "fan_2: " + this.fan_2 + ", " +
        "fan_3: " + this.fan_3 + ", " +
        "latitude: " + this.latitude + ", " +
        "longitude: " + this.longitude +
        "}" ;
    }
}
