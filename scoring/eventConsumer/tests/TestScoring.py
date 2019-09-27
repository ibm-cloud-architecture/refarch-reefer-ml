import unittest
from domain.predictservice import PredictService
import ScoringAgent as ScoringAgent

class TestScoring(unittest.TestCase):

    def testServiceCreation(self):
        serv = PredictService()
        self.assertIsNotNone(serv)

    def testPredict(self):
        serv = PredictService("domain/model_logistic_regression.pkl")
        header = "measurement_time,container_id, product_id,temperature,target_temperature, ambiant_temperature, kilowatts, time_door_open, content_type, defrost_cycle,oxygen_level, nitrogen_level, humidity_level, carbon_dioxide_level, vent_1, vent_2, vent_3"
        # poweroff event
        event="2019-09-25 02:42:33.573934, C01, P02, 6.369165267938210,	6, 21.40990035369160, 2.5141340338482900,	0.9917395739148560,	2,	5, 21.163197304339900,  1.3625605808523400, 25, 4.59426338168222, TRUE, TRUE,TRUE"
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

