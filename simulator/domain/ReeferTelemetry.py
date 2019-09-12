
class ReeferTelemetry:
    containerID = "C100"
    o2 = 4
    co2 = 0.13

    def co2InRange(self):
        return (self.co2 >= 0 and self.co2 <= 1)

        