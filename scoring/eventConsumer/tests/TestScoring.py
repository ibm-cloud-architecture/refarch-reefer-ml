import unittest
from domain.predictservice import PredictService
import ScoringAgent as ScoringAgent

class TestScoring(unittest.TestCase):

    def testServiceCreation(self):
        serv = PredictService()
        self.assertIsNotNone(serv)

    def testShouldHaveNoMaintenance(self):
        serv = PredictService("domain/model_logistic_regression.pkl")
        header = "temperature,target_temperature, ambiant_temperature, kilowatts, time_door_open, content_type, defrost_cycle, oxygen_level, nitrogen_level, humidity_level, carbon_dioxide_level, vent_1, vent_2, vent_3"
        # poweroff event
        event=" 6.369165267938210,	6, 21.40990035369160, 2.5141340338482900,	0,	2,	5, 21.163197304339900,  1.3625605808523400, 25, 4.59426338168222, 1,1,1"
        record=header+"\n"+event
        score = serv.predict(record)
        print(score)
        self.assertTrue( score == 0)

    def testShouldHaveMaintenanceOnCo2(self):
        serv = PredictService("domain/model_logistic_regression.pkl")
        header = "temperature,target_temperature, ambiant_temperature, kilowatts, time_door_open, content_type, defrost_cycle, oxygen_level, nitrogen_level, humidity_level, carbon_dioxide_level, vent_1, vent_2, vent_3"
        # poweroff event
        event="6.369165267938210, 6, 21.40990035369160, 2.5141340338482900,	0,	2,	5, 21.163197304339900,  1.3625605808523400, 25, 44, 1,1,1"
        record=header+"\n"+event
        score = serv.predict(record)
        print(score)
        self.assertTrue( score == 1)

    def testValidateMetricsValues(self):
        # some integer has bad character in string: see (6,) for a 6
        v=ScoringAgent.assessDataAreValid("('2019-08-25 T23:08 Z', 'C01', 'P02', 3.6762064797334673, 4.4, 20, 11.186957573693714, 0, 2, 5, (6,), 70, 40 ,3)")
        self.assertFalse(v)
        v=ScoringAgent.assessDataAreValid("('2019-08-25 T23:08 Z', 'C01', 'P02', 3.6762064797334673, 4.4, 20, 11.186957573693714, 0, 2, 5, 21, 70, 40, 3)")
        self.assertTrue(v)

if __name__ == '__main__':
    unittest.main()

