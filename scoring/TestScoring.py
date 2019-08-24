import unittest
from scoring.predictservice import PredictService

class TestScoreMetric(unittest.TestCase):
    def testCreation(self):
        serv = PredictService()

    def testPredict(self):
        serv = PredictService()
        header="""Timestamp, ID, Temperature(celsius), Target_Temperature(celsius), Power, PowerConsumption, ContentType, O2, CO2, Time_Door_Open, Maintenance_Required, Defrost_Cycle"""
        event="2019-04-01 T16:29 Z,1813, 101, 4.291843460900875,4.4,0,10.273342381017777,3,4334.920958996634,4.9631508046318755,1,0,6"""
        record=header+"\n"+event
        self.assertTrue(serv.predict(record)>=0)
        
if __name__ == '__main__':
    unittest.main()

