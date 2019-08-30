import pickle
import pandas as pd
import sklearn
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

class PredictService:
    '''
    Wrapper interface in front of the ML trained model
    '''

    model = pickle.load(open("domain/model_logistic_regression.pkl","rb"),encoding='latin1')
    
    
    def predict(self,metricEvent):
        '''
        Predict the maintenance from the metric sent. The metric is a string of comma separated values.
        See the feature column names and order 
        '''
        feature_cols = ['Temperature(celsius)','Target_Temperature(celsius)','Power','PowerConsumption','ContentType','O2','CO2','Time_Door_Open','Maintenance_Required','Defrost_Cycle']
        # Do some simple data transformation and reading to build X
        TESTDATA = StringIO(metricEvent)
        data = pd.read_csv(TESTDATA, sep=",")
        data.columns = data.columns.to_series().apply(lambda x: x.strip())
        X = data[feature_cols]
        # Return 1 if maintenance is required, 0 otherwise
        return self.model.predict(X)

    
