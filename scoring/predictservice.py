import pickle
import pandas as pd
import sklearn
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

class PredictService:
    model = pickle.load(open("model_logistic_regression.pkl","rb"),encoding='latin1')
    
    
    def predict(self,metricEvent):
        TESTDATA = StringIO(metricEvent)
        data = pd.read_csv(TESTDATA, sep=",")
        data.columns = data.columns.to_series().apply(lambda x: x.strip())
        feature_cols = ['Temperature(celsius)','Target_Temperature(celsius)','Power','PowerConsumption','ContentType','O2','CO2','Time_Door_Open','Maintenance_Required','Defrost_Cycle']
        # use the list to select a subset of the original DataFrame
        X = data[feature_cols]
        return self.model.predict(X)

    
