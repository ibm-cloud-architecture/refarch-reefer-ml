import unittest
import datetime
from domain.reefer_simulator import ReeferSimulator 


class TestReeferSimulator(unittest.TestCase):
    
    def testCreation(self):
        print("should have one instance")
        simul = ReeferSimulator()
        self.assertIsNotNone(simul)
    
    def testGeneratingPowerOff(self):
        simul = ReeferSimulator()
        df=simul.generatePowerOff(cid="101",nb_records = 10, tgood=4.4)
        self.assertIsNotNone(df)
        self.assertEqual(df.size, 120)  # nb of rows x nbr of columns
        print(df)

    def testGeneratingCo2(self):
        simul = ReeferSimulator()
        df=simul.generateCo2(cid="102",nb_records = 10, tgood=4.4)
        self.assertIsNotNone(df)
        self.assertEqual(df.size, 120)  # nb of rows x nbr of columns
        print(df)

    def testGenerateRecordsAtSea(self):
        simul = ReeferSimulator()
        values = simul.generatePowerOffTuples(cid="103",nb_records = 5, tgood=4)
        print(values)

    def testGenerateCO2tuples(self):
        simul = ReeferSimulator()
        values = simul.generateCo2Tuples(cid="103",nb_records = 5, tgood=4)
        print(values)

    def testGenerateRecordSpecificValues(self):
        simul = ReeferSimulator()
        Today= datetime.datetime.today()
        for i in range(10):
            (timestamp,pwr,pwrc, co2,o2,tdoor) = simul.generateRecordSpecificValues(Today,i,0)
            print((timestamp,pwr,pwrc, co2,o2,tdoor))

if __name__ == '__main__':
    unittest.main()

