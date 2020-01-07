package ibm.gse.kcontainer.scoring.infrastructure;

public class ScoringResult {
	
	public ScoringPrediction[] predictions;
	
	
	public ScoringResult() {}
	

	public ScoringPrediction[] getPredictions() {
		return predictions;
	}

	public void setPredictions(ScoringPrediction[] predictions) {
		this.predictions = predictions;
	}

}
