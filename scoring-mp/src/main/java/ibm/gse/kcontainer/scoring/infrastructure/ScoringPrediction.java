package ibm.gse.kcontainer.scoring.infrastructure;

public class ScoringPrediction {
		public String[] fields;
	    public Object[][] values;
		
	    public ScoringPrediction() {}
	    
		public String[] getFields() {
			return fields;
		}
		public void setFields(String[] fields) {
			this.fields = fields;
		}

		public Object[][] getValues() {
			return values;
		}

		public void setValues(Object[][] values) {
			this.values = values;
		}
}
