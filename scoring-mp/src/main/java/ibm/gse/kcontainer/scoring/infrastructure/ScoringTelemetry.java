package ibm.gse.kcontainer.scoring.infrastructure;

import ibm.gse.kcontainer.scoring.domain.Telemetry;
import com.google.gson.Gson;
import com.google.gson.JsonParser;
import com.google.gson.JsonObject;
import com.google.gson.JsonArray;


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
		"defrost_cycle",
		"oxygen_level", 
		"nitrogen_level", 
		"humidity_level",
		"target_humidity_level",
		"carbon_dioxide_level", 
		"fan_1", "fan_2", "fan_3"};
	
		String[] fields = FEATURE_NAMES;
		Object[][] values = new Object[1][14];
	
		public ScoringTelemetry() {}
		
		public ScoringTelemetry(Telemetry inEvent) {
			values[0][0] = inEvent.getTemperature();
			values[0][1] = inEvent.getTarget_temperature();
			values[0][2] = inEvent.getAmbiant_temperature();
			values[0][3] = inEvent.getKilowatts();
			values[0][4] = inEvent.getTime_door_open();
			values[0][5] = inEvent.getDefrost_cycle();
			values[0][6] = inEvent.getOxygen_level();
			values[0][7] = inEvent.getNitrogen_level();
			values[0][8] = inEvent.getHumidity_level();
			values[0][9] = inEvent.getTarget_humidity_level();
			values[0][10] = inEvent.getCarbon_dioxide_level();
			values[0][11] = inEvent.isFan_1();
			values[0][12] = inEvent.isFan_2();
			values[0][13] = inEvent.isFan_3();
		}
	
		public Object[][] getValues() {
			return values;
		}
	
		public void setValues(Object[][] values) {
			this.values = values;
		}
	
		public String[] getFields() {
			return fields;
		}
}