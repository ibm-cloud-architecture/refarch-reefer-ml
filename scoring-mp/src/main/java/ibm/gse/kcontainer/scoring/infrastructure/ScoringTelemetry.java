package ibm.gse.kcontainer.scoring.infrastructure;

public class ScoringTelemetry {
    public static final String[] FEATURE_NAMES = { 
    "temperature",
    "target_temperature", 
    "ambiant_temperature", 
    "kilowatts", 
    "time_door_open",
    "content_type", 
    "defrost_cycle",
    "oxygen_level", 
    "nitrogen_level", 
    "humidity_level","target_humidity_level", 
    "carbon_dioxide_level", 
    "fan_1", "fan_2", "fan_3"};

    String[] fields = FEATURE_NAMES;
    String[][] values = {};

}