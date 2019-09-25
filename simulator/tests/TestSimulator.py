import unittest
import datetime
from simulator.domain.reefer_simulator import ReeferSimulator 


class TestReeferSimulator(unittest.TestCase):
    
    def testCreation(self):
        print("should have one instance")
        simul = ReeferSimulator()
        self.assertIsNotNone(simul)
    
    def testGeneratingPowerOff(self):
        simul = ReeferSimulator()
        df=simul.generatePowerOffRecords(cid="101",nb_records = 100, product_id= "P02")
        self.assertIsNotNone(df)
        self.assertEqual(df.size, 1700)  # nb of rows x nbr of columns
        print(df)

    def testGeneratingCo2(self):
        simul = ReeferSimulator()
        df=simul.generateCo2Records(cid="102",nb_records = 100, product_id= "P02")
        self.assertIsNotNone(df)
        self.assertEqual(df.size, 1700)  # nb of rows x nbr of columns
        print(df)

    def testGenerateRecordsAtSea(self):
        simul = ReeferSimulator()
        values = simul.generatePowerOffTuples(cid="103",nb_records = 5, product_id= "P02")
        print(values)

    def testGenerateCO2tuples(self):
        simul = ReeferSimulator()
        values = simul.generateCo2Tuples(cid="103",nb_records = 5, product_id= "P02")
        print(values)

if __name__ == '__main__':
    unittest.main()

