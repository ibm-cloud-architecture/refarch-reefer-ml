import unittest
import datetime
import json
from simulator.domain.reefer_simulator import ReeferSimulator 


class TestReeferSimulator(unittest.TestCase):
    
    def testCreation(self):
        print("should have one instance")
        simul = ReeferSimulator()
        self.assertIsNotNone(simul)
    
    def testNormalRecords(self):
        simul = ReeferSimulator()
        df=simul.generateNormalRecords(nb_records = 4)
        self.assertIsNotNone(df)
        for idx, content in df.items():
            print(content)

    def testGeneratingPowerOff(self):
        simul = ReeferSimulator()
        df=simul.generatePowerOffRecords(cid="C01",nb_records = 100, product_id= "P02")
        self.assertIsNotNone(df)
        self.assertEqual(df.size, 2000)  # nb of rows x nbr of columns
        df2 = df.loc[df['maintenance_required'] == 1]
        for idx, content in df2.items():
            print(content)
        

    def testGeneratingCo2(self):
        simul = ReeferSimulator()
        df=simul.generateCo2Records(cid="C01",nb_records = 100, product_id= "P02")
        self.assertIsNotNone(df)
        self.assertEqual(df.size, 2000)  # nb of rows x nbr of columns


    def testGenerateO2(self):
        simul = ReeferSimulator()
        values = simul.generateO2Tuples(cid="C01",nb_records = 100, product_id= "P02")
        

    def testGenerateCO2tuples(self):
        simul = ReeferSimulator()
        values = simul.generateCo2Tuples(cid="C02",nb_records = 10, product_id= "P03")
        for value in values:
            print(value)

if __name__ == '__main__':
    unittest.main()

