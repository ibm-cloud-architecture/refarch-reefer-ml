package ibm.gse.kcontainer.scoring.infrastructure;

import ibm.gse.kcontainer.scoring.domain.Telemetry;

/**
 * This is the input to WML deployed scoring service
 * @author jeromeboyer
 *
 */
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
    "humidity_level",
    "target_humidity_level", 
    "carbon_dioxide_level", 
    "fan_1", "fan_2", "fan_3"};

    String[] fields = FEATURE_NAMES;
    String[][] values = new String[1][15];

    public ScoringTelemetry() {}
    
    public ScoringTelemetry(Telemetry inEvent) {
    	values[0][0] = Double.toString(inEvent.getTemperature());
    	values[0][1] = Double.toString(inEvent.getTarget_temperature());
    	values[0][2] = Double.toString(inEvent.getAmbiant_temperature());
    	values[0][3] = Double.toString(inEvent.getKilowatts());
    	values[0][4] = Double.toString(inEvent.getTime_door_open());
    	values[0][5] = Integer.toString(inEvent.getContent_type());
    	values[0][6] = Integer.toString(inEvent.getDefrost_cycle());
    	values[0][7] = Double.toString(inEvent.getOxygen_level());
    	values[0][8] = Double.toString(inEvent.getNitrogen_level());
    	values[0][9] = Double.toString(inEvent.getHumidity_level());
    	values[0][10] = Double.toString(inEvent.getTarget_humidity_level());
    	values[0][11] = Double.toString(inEvent.getCarbon_dioxide_level());
    	values[0][12] = Boolean.toString(inEvent.isFan_1());
    	values[0][13] = Boolean.toString(inEvent.isFan_2());
    	values[0][14] = Boolean.toString(inEvent.isFan_3());
    }

	public String[][] getValues() {
		return values;
	}

	public void setValues(String[][] values) {
		this.values = values;
	}

	public String[] getFields() {
		return fields;
	}
}