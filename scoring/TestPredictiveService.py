import urllib3, requests, json
from requests.auth import HTTPBasicAuth
import os

USERNAME = os.getenv("cp4d_user", "admin")
PASSWORD = os.getenv("cp4d_pwd", "")
BASE_URL = os.getenv("PREDICTION_BASE_URL", "https://zen-cpd-zen.apps.demo2.demo.ibmcloud.com")
PREDICTION_URL = os.getenv("PREDICTION_URL", "")

def getIAMtoken(cluster_creds):
    response = requests.get(
        u'{}/v1/preauth/validateAuth'.format(cluster_creds['url']),
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        },
        auth=HTTPBasicAuth(cluster_creds['username'], cluster_creds['password']),
        verify=False)
    iam_token = response.json()['accessToken']
    return iam_token

cluster_creds={ "url": BASE_URL,
"username" : USERNAME,
"password" : PASSWORD
}
mltoken = getIAMtoken(cluster_creds)

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
FEATURE_NAMES = [ "temperature",
                "target_temperature", 
                "ambiant_temperature", 
                "kilowatts", 
                "time_door_open",
                "defrost_cycle",
                "oxygen_level", 
                "nitrogen_level", 
                "humidity_level",
                "carbon_dioxide_level", 
                "FAN_1", "FAN_2", "FAN_3"]
payload_scoring = {"input_data": [{
    "fields": FEATURE_NAMES, 
    "values": [[8,4,25,2,0,2,5,12,78,60,50,10,True,True,True]]
    }
    ]}
response_scoring = requests.post(BASE_URL + PREDICTION_URL, json=payload_scoring,verify=False, headers=header)
print("Scoring response")
print(json.loads(response_scoring.text))