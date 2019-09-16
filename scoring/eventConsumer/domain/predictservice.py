import pickle
import pandas as pd
import requests
import sys, os
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO


# this is use in case we want to have the model running on a remote server instead of using 
# the one embedded. 
try:
    SCORING_URL = os.environ['SCORING_URL']
except KeyError:
    SCORING_URL=''  # be sure to keep it empty


class PredictService:
    '''
    Wrapper interface in front of the ML trained model
    '''
    def __init__(self,filename = "domain/model_logistic_regression.pkl"):
        self.model = pickle.load(open(filename,"rb"),encoding='latin1')
    
    
    def predict(self,metricEvent):
        '''
        Predict the maintenance from the telemetry sent. The telemetry is a string of comma separated values.
        See the feature column names and order below.
        return 0 if no maintenance is needed, 1 otherwise
        '''
        feature_cols = ['Temperature(celsius)','Target_Temperature(celsius)','Power','PowerConsumption','ContentType','O2','CO2','Time_Door_Open','Maintenance_Required','Defrost_Cycle']
        # Do some simple data transformation and reading to build X
        TESTDATA = StringIO(metricEvent)
        data = pd.read_csv(TESTDATA, sep=",")
        data.columns = data.columns.to_series().apply(lambda x: x.strip())
        X = data[feature_cols]
        # Return 1 if maintenance is required, 0 otherwise
        if (SCORING_URL != ''):
            return requests.post(url=SCORING_URL, data= X)
        else:
            return self.model.predict(X)

    
