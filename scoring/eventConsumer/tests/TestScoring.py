import unittest
from domain.predictservice import PredictService
import ScoringApp as ScoringApp

class TestScoring(unittest.TestCase):

    def testServiceCreation(self):
        serv = PredictService()
        self.assertIsNotNone(serv)

    def testPredict(self):
        serv = PredictService("domain/model_logistic_regression.pkl")
        header="Timestamp, ID, Temperature(celsius), Target_Temperature(celsius), Power, PowerConsumption, ContentType, O2, CO2, Time_Door_Open, Maintenance_Required, Defrost_Cycle"
        event="2019-04-01 T16:29 Z,1813, 101, 4.291843460900875,4.4,0,10.273342381017777,3,4334.920958996634,4.9631508046318755,1,0,6"
        record=header+"\n"+event
        self.assertTrue(serv.predict(record)>=0)

    def testValidateMetricsValues(self):
        # some integer has bad character in string: see (6,) for a 6
        v=ScoringApp.assessDataAreValid("('2019-08-25 T23:08 Z', 'c100', 3.6762064797334673, 4.4, 11.186957573693714, 4.822553994902155, 5, (6,), -0.5235016159318118, (5.036643236673223,), 0, 4)")
        self.assertFalse(v)
        v=ScoringApp.assessDataAreValid("('2019-08-25 T23:08 Z', 'c100', 3.6762064797334673, 4.4, 11.186957573693714, 4.822553994902155, 5, 6, -0.5235016159318118, 5.036643236673223, 0, 4)")
        self.assertTrue(v)

if __name__ == '__main__':
    unittest.main()

