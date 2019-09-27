import pickle
import pandas as pd
import requests
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

# Attention it will be tempting to use the column names defined in the simulator, but in reality
# those two codes are unrelated, and the definition comes from the data... Each services are coded
# by different teams and they know about the data not the code. 
FEATURES_NAMES = [ "temperature","target_temperature", "ambiant_temperature", 
                "kilowatts", "time_door_open",
                "content_type", "defrost_cycle",
                "oxygen_level", "nitrogen_level", "humidity_level","carbon_dioxide_level", 
                "vent_1", "vent_2", "vent_3"]

class PredictService:
    '''
    Wrapper interface in front of the ML trained model
    '''
    def __init__(self,filename = "domain/model_logistic_regression.pkl"):
        self.model = pickle.load(open(filename,"rb"),encoding='latin1')
    
    
    def predict(self,metricEvent):
        '''
        Predict the maintenance from the telemetry event received. The telemetry is a string of comma separated values.
        See the feature column names and order below.
        return 0 if no maintenance is needed, 1 otherwise
        '''
        # Do some simple data transformation and reading to build X
        TESTDATA = StringIO(metricEvent)
        data = pd.read_csv(TESTDATA, sep=",")
        data.columns = data.columns.to_series().apply(lambda x: x.strip())
        X = data[FEATURES_NAMES]
        # Return 1 if maintenance is required, 0 otherwise
        return self.model.predict(X)

    
