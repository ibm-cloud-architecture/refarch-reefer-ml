import unittest
from simulator.domain.ReeferTelemetry import ReeferTelemetry



class TestReeferTelemetry(unittest.TestCase):
 
    def testTelemetryCreation(self):
        print("should have one instance")
        metric = ReeferTelemetry()
        self.assertIsNotNone(metric)
        self.assertEqual(metric.co2, 0.13)
        self.assertTrue(metric.co2InRange())

    def testCo2Value(self):
        metric = ReeferTelemetry()
        print("should have co2 sensor as percent")
        metric.co2=1.3
        self.assertFalse(metric.co2InRange())

    

if __name__ == '__main__':
    unittest.main()
