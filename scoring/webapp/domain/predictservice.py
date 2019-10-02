import pickle
import pandas as pd
import sys, os
from minio import Minio
import re
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

bucket_name = os.getenv('BUCKET_NAME', 'training-data')
model_path = os.getenv('MODEL_PATH', 'model_logistic_regression.pkl')
S3_ENDPOINT = os.getenv('S3_ENDPOINT', 'minio-service.kubeflow:9000')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'minio')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'minio123')

class PredictService:
    '''
    Wrapper interface in front of the ML trained model
    '''
    url = re.compile(r"https?://")
    cos = Minio(url.sub('', S3_ENDPOINT),
                access_key=AWS_ACCESS_KEY_ID,
                secret_key=AWS_SECRET_ACCESS_KEY,
                secure=False)
    cos.fget_object(bucket_name, model_path, 'domain/model_logistic_regression.pkl')

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
