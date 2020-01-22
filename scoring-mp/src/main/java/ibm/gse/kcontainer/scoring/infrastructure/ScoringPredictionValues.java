package ibm.gse.kcontainer.scoring.infrastructure;

public class ScoringPredictionValues {
	
	public String prediction;
	public Double[] metrics;
	
	public ScoringPredictionValues() {};
	public ScoringPredictionValues(Object[][] input) {
		this.prediction = input[0][0].toString();
		String [] temp = input[0][1].toString().replace("[", "").replace("]", "").split(",");
		this.metrics = new Double[2];
		this.metrics[0] = Double.valueOf(temp[0]);
		this.metrics[1] = Double.valueOf(temp[1]);
	}

	public String getPrediction(){
		return this.prediction;
	}

	public void setPrediction(String prediction){
		this.prediction = prediction;
	}

	public Double[] getMetrics(){
		return this.metrics;
	}

	public void setMetrics(Double[] metrics){
		this.metrics = metrics;
	}
}
