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
public class ScoringTelemetryWrapper {

    ScoringTelemetry[] input_data = new ScoringTelemetry[1];

    public ScoringTelemetryWrapper() {}
    
    public ScoringTelemetryWrapper(ScoringTelemetry sc) {
    	input_data[0] = sc;
    }

	public ScoringTelemetry[] getInputData() {
		return input_data;
	}

	public void setInputData(ScoringTelemetry[] input) {
		this.input_data = input;
	}
}