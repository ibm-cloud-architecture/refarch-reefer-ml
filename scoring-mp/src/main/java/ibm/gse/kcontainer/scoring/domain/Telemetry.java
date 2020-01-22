package ibm.gse.kcontainer.scoring.domain;

public class Telemetry {
    String container_id;
    String measurement_time;
    String product_id;
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
    double target_humidity_level;
    double carbon_dioxide_level; 
    boolean fan_1; 
    boolean fan_2; 
    boolean fan_3;
    double latitude;
    double longitude;
    int maintenance_required;

    public Telemetry(){
        
    }

    public Telemetry(String payload){
        String [] arrayValues = payload.replace("(", "").replace(")", "").replace("'", "").split(",");
        if (arrayValues.length == 20){
            this.container_id = arrayValues[0].trim();
            this.measurement_time = arrayValues[1].trim();
            this.product_id = arrayValues[2].trim();
            this.temperature = Double.parseDouble(arrayValues[3].trim());
            this.target_temperature = Double.parseDouble(arrayValues[4].trim());
            this.ambiant_temperature = Double.parseDouble(arrayValues[5].trim());
            this.kilowatts = Double.parseDouble(arrayValues[6].trim());
            this.time_door_open = Double.parseDouble(arrayValues[7].trim());
            this.content_type = Integer.parseInt(arrayValues[8].trim());
            this.defrost_cycle = Integer.parseInt(arrayValues[9].trim());
            this.oxygen_level = Double.parseDouble(arrayValues[10].trim());
            this.nitrogen_level = Double.parseDouble(arrayValues[11].trim());
            this.humidity_level = Double.parseDouble(arrayValues[12].trim());
            this.target_humidity_level = Double.parseDouble(arrayValues[12].trim());
            this.carbon_dioxide_level = Double.parseDouble(arrayValues[13].trim());
            this.fan_1 = Boolean.valueOf(arrayValues[14].trim());
            this.fan_2 = Boolean.valueOf(arrayValues[15].trim());
            this.fan_3 = Boolean.valueOf(arrayValues[16].trim());
            this.latitude = Double.parseDouble(arrayValues[17].trim());
            this.longitude = Double.parseDouble(arrayValues[18].trim());
            this.maintenance_required = Integer.parseInt(arrayValues[19].trim());
        }
    }
    
    public String getContainerID(){
        return this.container_id;
    }

    public void setContainerID(String containerID){
        this.container_id=containerID;
    }

    public String getMeasurementTime(){
        return this.measurement_time;
    }

    public void setMeasurementTime(String measurementTime){
        this.measurement_time=measurementTime;
    }

    public String getProductID(){
        return this.product_id;
    }

    public void setProductID(String productID){
        this.product_id=productID;
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

    public double getTarget_humidity_level() {
        return target_humidity_level;
    }

    public void setTarget_humidity_level(double target_humidity_level) {
        this.target_humidity_level = target_humidity_level;
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

    public int getMaintenanceRequired(){
        return this.maintenance_required;
    }

    public void setMaintenanceRequired(int maintenance){
        this.maintenance_required=maintenance;
    }

    public String toString(){
        return "{" +
        "container_id: " + this.container_id + ", " +
        "measurement_time: " + this.measurement_time + ", " +
        "product_id: " + this.product_id + ", " +
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
        "target_humidity_level: " + this.target_humidity_level + ", " +
        "carbon_dioxide_level: " + this.carbon_dioxide_level + ", " +
        "fan_1: " + this.fan_1 + ", " +
        "fan_2: " + this.fan_2 + ", " +
        "fan_3: " + this.fan_3 + ", " +
        "latitude: " + this.latitude + ", " +
        "longitude: " + this.longitude + ", " +
        "maintenance_required: " + this.maintenance_required +
        "}" ;
    }
}
