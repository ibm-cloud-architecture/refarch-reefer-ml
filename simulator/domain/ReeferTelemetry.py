
'''
'''

class ReeferTelemetry:
    containerID = "C100"
    o2 = 4
    co2 = 0.13
    measurement_time TIMESTAMP NOT NULL,
    productID varchar(64) NOT NULL,
    temperature REAL,
    target_temperature REAL,
    ambiant_temperature REAL, 
    kilowatts REAL,
    kilowatt_hours REAL,
    content_type INT,
    oxygen_level REAL,
    nitrogen REAL,
    vent_1 BOOLEAN,
    vent_2 BOOLEAN,
    vent_3 BOOLEAN,
    carbon_dioxide_level REAL,
    time_door_open REAL,
    location POINT,
    defrost_cycle INT,

    def co2InRange(self):
        return (self.co2 >= 0 and self.co2 <= 1)

        