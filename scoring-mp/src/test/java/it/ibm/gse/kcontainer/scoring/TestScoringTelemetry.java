package it.ibm.gse.kcontainer.scoring;

import java.math.BigDecimal;
import java.util.List;

import javax.json.bind.Jsonb;
import javax.json.bind.JsonbBuilder;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import com.google.gson.Gson;

import ibm.gse.kcontainer.scoring.domain.Telemetry;
import ibm.gse.kcontainer.scoring.infrastructure.ScoringClient;
import ibm.gse.kcontainer.scoring.infrastructure.ScoringPrediction;
import ibm.gse.kcontainer.scoring.infrastructure.ScoringPredictionValues;
import ibm.gse.kcontainer.scoring.infrastructure.ScoringResult;
import ibm.gse.kcontainer.scoring.infrastructure.ScoringTelemetry;


public class TestScoringTelemetry {

   Telemetry telemetryEvent;
   
   @Before
   public void createData() {
	   telemetryEvent = new Telemetry();
	   telemetryEvent.setHumidity_level(.4);
       telemetryEvent.setKilowatts(10);
       telemetryEvent.setNitrogen_level(.5);
       telemetryEvent.setTarget_temperature(6);
       telemetryEvent.setTemperature(5);
       telemetryEvent.setTime_door_open(0);
       telemetryEvent.setOxygen_level(.6);
       telemetryEvent.setAmbiant_temperature(20);
       telemetryEvent.setCarbon_dioxide_level(.3);
       telemetryEvent.setContent_type(1);
       telemetryEvent.setDefrost_cycle(6);
       telemetryEvent.setFan_1(true);
       telemetryEvent.setFan_2(true);
       telemetryEvent.setFan_3(true);
   }
   
    @Test
    public void testEnvVariables() {
        Assert.assertTrue("jboyer".equals(System.getenv("cp4d_user")));
        Assert.assertNotNull(System.getenv("PREDICTION_BASE_URL"));
    }

   // @Test
    public void testGetIAMToken(){
        final ScoringClient sc = new ScoringClient(System.getenv("PREDICTION_BASE_URL"),System.getenv("cp4d_user"),System.getenv("cp4d_pwd"));
        Assert.assertNotNull(sc.getIAMToken());
    }

    @Test
    public void shouldCreateTelemetryParameterFromEvent() {
    	ScoringTelemetry sc = new ScoringTelemetry(telemetryEvent);
    	Assert.assertTrue(sc.getFields().length == 15);
    	for (String column : sc.getFields()) {
    		System.out.println(column);
    	}
    	Assert.assertTrue(sc.getValues()[0].length == 15);
    	for (int i = 0; i< 15 ; i++) {
    		System.out.println(sc.getValues()[0][i]);
    	}
    }
    
    @Test
    public void shouldCreateJsonStringFromScoringResult() {
    	ScoringResult sr = new ScoringResult();
    	sr.predictions= new ScoringPrediction[1];
    	sr.predictions[0] = new ScoringPrediction();
        sr.predictions[0].fields = new String[] {"prediction", "probability"};
        ScoringPredictionValues spv = new ScoringPredictionValues();
        spv.prediction = "N";
        spv.metrics = new Double[2];
        spv.metrics[0] = new Double(0.7);
        spv.metrics[1] = new Double(0.7);
    	sr.predictions[0].values = new ScoringPredictionValues[1][1];
    	sr.predictions[0].values[0][0] = spv;
   	  	// List<BigDecimal> vs = new ArrayList<BigDecimal>();
   	  	// vs.add(0, new BigDecimal(0.7));
   	  	// vs.add(1,new BigDecimal(0.7));
   	  	// sr.predictions[0].values[0][1] = vs;
   	  	Gson parser = new Gson();
   	  	System.out.println(parser.toJson(sr));
   	  	// the following code is generating an exception I was not able to fix quickly.
    	//Jsonb jsonb = JsonbBuilder.create();
    	//System.out.println(jsonb.toJson(sr));
    }
    
    @Test
    @SuppressWarnings("unchecked")
    public void shouldCreateScoringResult() {
    	// this approach is using jsonb
    	String inJson = "{\"predictions\": [{\"fields\": [\"prediction\", \"probability\"],\"values\": [[\"N\", [0.6555252075195312, 0.34447482228279114]]]}]}";
   	  	Jsonb jsonb = JsonbBuilder.create();
   	  	ScoringResult sc = jsonb.fromJson(inJson, ScoringResult.class);
   	  	Assert.assertTrue(sc.predictions.length == 1);
   	  	Assert.assertTrue("prediction".contentEquals(sc.predictions[0].fields[0]));
   	  	Assert.assertTrue("N".equals(sc.predictions[0].values[0][0]));
   	  	List<BigDecimal> vs = (List<BigDecimal>) sc.predictions[0].values[0][1];
   	    Assert.assertTrue(0.6555252075195312 == vs.get(0).doubleValue());
  
   	    // can do the same with Gson...simpler
   	    Gson parser = new Gson();
   	    sc = parser.fromJson(inJson, ScoringResult.class);
   		Assert.assertTrue("N".equals(sc.predictions[0].values[0][0]));
    }
    
    @Test
    public void shouldNotHaveAnomalyWithGoodData(){
        final ScoringClient sc = new ScoringClient(System.getenv("PREDICTION_BASE_URL"),System.getenv("cp4d_user"),System.getenv("cp4d_pwd"));
        sc.setPredictiveURL(System.getenv("PREDICTION_URL"));
        final ScoringResult r = sc.callAnomalyScoring(telemetryEvent);
        Assert.assertNotNull(r);
        sc.close();
    }
}