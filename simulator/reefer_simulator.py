import csv, sys, json, datetime
import random
import numpy as np
import pandas as pd
import os

'''
Simulate the metrics for a Reefer container.
'''
# Define constants for average
POWEROFF_SIMUL="poweroff"
CO2_SIMUL="co2sensor"
CO2_LEVEL = 4 # in %
O2_LEVEL = 21 # in %
NITROGEN_LEVEL = 0.78 # in %
POWER_LEVEL= 7.2 # in kW
NB_RECORDS_IMPACTED = 7
MAX_RECORDS = 1000

class ReeferSimulator:
    def defineDataFrame(self):
        return pd.DataFrame(columns=['Timestamp', 'ID', 'Temperature(celsius)', 'Target_Temperature(celsius)', 'Power', 'PowerConsumption', 'ContentType', 'O2', 'CO2', 'Time_Door_Open', 
    'Maintenance_Required', 'Defrost_Cycle'])

    def generatePowerOff(self,cid="101",nb_records = MAX_RECORDS, tgood=4.4):
        df = self.defineDataFrame()
        range_list=np.linspace(1,2,nb_records)
        ctype=random.randint(1,5)   # ContentType
        print("Generating ",nb_records, " poweroff metrics")
        count_pwr = 0  # generate n records with power off
        
        temp = random.gauss(tgood, 2.0)
        Today= datetime.datetime.today()
        for i in range_list:
            adate = Today + datetime.timedelta(minutes=15*i)
            timestamp =  adate.strftime('%Y-%m-%d T%H:%M Z')
            oldtemp = temp
            temp =  random.gauss(tgood, 2.0)
            pwr =  random.gauss(POWER_LEVEL,8)   # Power at this time - 
            # as soon as one amp record < 0 then poweroff for n records
            maintenance_flag = 0
            if  pwr < 0.0:
                pwr = 0
                count_pwr = count_pwr + 1
                temp = oldtemp
            elif 0 < count_pwr < NB_RECORDS_IMPACTED:
                # when powerer off the T increase
                count_pwr = count_pwr + 1
                pwr = 0
                temp = oldtemp + 0.8 * count_pwr
            if count_pwr == NB_RECORDS_IMPACTED:
                maintenance_flag = 1
                count_pwr = 0
            df.loc[i] = [timestamp, 
                        cid,
                        temp, # Temperature(celsius)
                        tgood,             # Target_Temperature(celsius)
                        pwr,    
                        random.gauss(POWER_LEVEL,1.0), # PowerConsumption
                        ctype,                # ContentType
                        random.randrange(O2_LEVEL),  # O2
                        random.randrange(CO2_LEVEL), # CO2
                        random.gauss(8.0, 2.0), # Time_Door_Open
                        maintenance_flag,    # maintenance required
                        6]    # defrost cycle

        return df    
        
 
    # Generate data if co2 sensor malfunctions
    def generateCo2(self,cid="101", nb_records= MAX_RECORDS, tgood=4.4):
        df = self.defineDataFrame()
        range_list=np.linspace(1,2,nb_records)
        ctype=random.randint(1,5)   # ContentType
        print("Generating ",nb_records, " Co2 metrics")
        temp = random.gauss(tgood, 3.0)
        Today= datetime.datetime.today()
        for i in range_list:
            maintenance_flag = 0
            adate = Today + datetime.timedelta(minutes=15*i)
            timestamp =  adate.strftime('%Y-%m-%d T%H:%M Z')
            pwr =  random.gauss(POWER_LEVEL,8)
            co2 = random.gauss(3.5, 3.0)
            if co2>CO2_LEVEL or co2<0:
                maintenance_flag = 1
            df.loc[i] = [timestamp, 
                        cid, # Container ID
                        temp, # Temperature(celsius)
                        tgood, # Target_Temperature(celsius)
                        pwr,
                        random.gauss(POWER_LEVEL,1.0), # PowerConsumption
                        ctype,# ContentType
                        random.randrange(O2_LEVEL),  # O2
                        co2, # CO2
                        random.gauss(8.0, 2.0), # Time_Door_Open
                        maintenance_flag, # maintenance required
                        6] # defrost cycle
        return df
