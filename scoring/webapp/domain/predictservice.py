import pickle
import pandas as pd
import sys, os
import re
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
        Predict the maintenance from the telemetry sent. The telemetry is a string of comma separated values.
        See the feature column names and order below.
        return 0 if no maintenance is needed, 1 otherwise
        '''
        feature_cols = ['temperature','target_temperature','ambiant_temperature','oxygen_level','carbon_dioxide_level','humidity_level','nitrogen_level','vent_1','vent_2','vent_3','kilowatts','content_type','time_door_open','defrost_cycle']
        # Do some simple data transformation and reading to build X
        TESTDATA = StringIO(metricEvent)
        data = pd.read_csv(TESTDATA, sep=",")
        data.columns = data.columns.to_series().apply(lambda x: x.strip())
        X = data[feature_cols]
        # Return 1 if maintenance is required, 0 otherwise
        return self.model.predict(X)
