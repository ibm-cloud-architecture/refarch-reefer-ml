import unittest
from simulator.reefer_simulator import ReeferSimulator 


class TestReeferSimulator(unittest.TestCase):
    
    def testCreation(self):
        print("should have one instance")
        simul = ReeferSimulator()
        self.assertIsNotNone(simul)
    
    def testGeneratingPowerOff(self):
        simul = ReeferSimulator()
        df=simul.generatePowerOff(cid="101",nb_records = 10, tgood=4.4)
        self.assertIsNotNone(df)
        self.assertEquals(df.size, 120)  # nb of rows x nbr of columns
        print(df)

    def testGeneratingCo2(self):
        simul = ReeferSimulator()
        df=simul.generateCo2(cid="101",nb_records = 10, tgood=4.4)
        self.assertIsNotNone(df)
        self.assertEquals(df.size, 120)  # nb of rows x nbr of columns
        print(df)

if __name__ == '__main__':
    unittest.main()

