import csv, sys, json, datetime
import random
import numpy as np
import pandas as pd
import os

'''
Simulate the metrics for a Reefer container according to the type of simulation.
Each simulation type is a different method.
The variables that changes are Co2, O2, power and temperature

This code could be refactored to avoid code duplication.

'''
# Define constants for average

CO2_LEVEL = 4 # in %
O2_LEVEL = 21 # in %
NITROGEN_LEVEL = 0.78 # in %
POWER_LEVEL= 7.2 # in kW
NB_RECORDS_IMPACTED = 7
MAX_RECORDS = 1000
DEFROST_LEVEL = 7

class ReeferSimulator:
    SIMUL_POWEROFF="poweroff"
    SIMUL_CO2="co2sensor"
    # Some method use pandas dataframe
    def defineDataFrame(self):
        return pd.DataFrame(columns=['Timestamp', 'ID', 'Temperature(celsius)', 'Target_Temperature(celsius)', 'Power', 'PowerConsumption', 'ContentType', 'O2', 'CO2', 'Time_Door_Open', 
    'Maintenance_Required', 'Defrost_Cycle'])


    def generateCommonValues(self,tgood=4.4):
        ctype=random.randint(1,5)   # ContentType
        temp = random.gauss(tgood, 3.0)
        Today= datetime.datetime.today()
        return (Today,ctype,temp)

    def generateRecordSpecificValues(self,Today,idx,pwrc_in):
        adate = Today + datetime.timedelta(minutes=15*idx)
        timestamp =  adate.strftime('%Y-%m-%d T%H:%M Z')
        pwr =  random.gauss(POWER_LEVEL,6)    # Power
        if pwrc_in == 0:
            pwrc = random.gauss(POWER_LEVEL,10.0)  # PowerConsumption
        else:
            pwrc=pwr+pwrc_in
        co2 = random.gauss(CO2_LEVEL, 3.0)
        o2 = random.gauss(O2_LEVEL,3.0)  # O2
        tdoor = random.gauss(30.0, 2.0) # Time_Door_Open
        return (timestamp,pwr,pwrc,co2,o2,tdoor)


    def generatePowerOffTuples(self,cid="101",nb_records = MAX_RECORDS, tgood=4.4):
        '''
        Generate an array of tuples with reefer container values
        '''
        count_pwr = 0  # generate n records with power off
        (Today,ctype,temp) = self.generateCommonValues(tgood)
        records = []
        pwrc=0
        for i in range(nb_records):
            oldtemp = temp
            (timestamp,pwr,pwrc, co2,o2,tdoor) = self.generateRecordSpecificValues(Today,i,pwrc)  
            temp =  random.gauss(tgood, 2.0)
            # as soon as one record power < 0 then poweroff for n records
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
                count_pwr = 0
                pwrc=0
            records.append((timestamp,
                        cid,
                        temp,tgood,
                        pwr, pwrc,
                        ctype,                # ContentType
                        o2,  # O2
                        co2, # CO2
                        tdoor, 
                        0,    # maintenance required
                        random.randrange(DEFROST_LEVEL)))
        return records

    
    def generatePowerOff(self,cid="101",nb_records = MAX_RECORDS, tgood=4.4):
        '''
        Generate n records for training and test set for the power off simulation.
        Power off will be off for NB_RECORDS_IMPACTED events
        '''
        print("Generating ",nb_records, " poweroff metrics")
        count_pwr = 0  # generate n records with power off
        (Today,ctype,temp) = self.generateCommonValues(tgood)
        df = self.defineDataFrame()
        pwrc=0
        for i in range(nb_records):
            oldtemp = temp
            (timestamp,pwr,pwrc, co2,o2,tdoor) = self.generateRecordSpecificValues(Today,i,pwrc)
            temp =  random.gauss(tgood, 2.0)
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
                # when it reaches n records at power 0 time to flag it
                maintenance_flag = 1
                count_pwr = 0
                pwrc=0
            df.loc[i] = [timestamp, 
                        cid,
                        temp, # Temperature(celsius)
                        tgood,             # Target_Temperature(celsius)
                        pwr,    
                        pwrc, # PowerConsumption
                        ctype,                # ContentType
                        o2,  # O2
                        co2, # CO2
                        tdoor, # Time_Door_Open
                        maintenance_flag,    # maintenance required
                        random.randrange(DEFROST_LEVEL)]    # defrost cycle

        return df    
        

 
    # Generate data if co2 sensor malfunctions
    def generateCo2(self,cid="101", nb_records= MAX_RECORDS, tgood=4.4):
        (Today,ctype,temp) = self.generateCommonValues(tgood)
        df = self.defineDataFrame()
        pwrc=0
        for i in range(nb_records):
            maintenance_flag = 0
            (timestamp,pwr,pwrc, co2,o2,tdoor) = self.generateRecordSpecificValues(Today,i,pwrc);        
            if co2>CO2_LEVEL or co2<0:
                maintenance_flag = 1
            df.loc[i] = [timestamp, 
                        cid, # Container ID
                        temp, # Temperature(celsius)
                        tgood, # Target_Temperature(celsius)
                        pwr,
                        pwrc, # PowerConsumption
                        ctype,# ContentType
                        o2,
                        co2, # CO2
                        tdoor, # Time_Door_Open
                        maintenance_flag, # maintenance required
                        random.randrange(DEFROST_LEVEL)] # defrost cycle
        return df

    def generateCo2Tuples(self,cid="101", nb_records= MAX_RECORDS, tgood=4.4):
        (Today,ctype,temp) = self.generateCommonValues(tgood)
        records = []
        pwrc=0
        for i in range(nb_records):
            (timestamp,pwr,pwrc, co2,o2,tdoor) = self.generateRecordSpecificValues(Today,i,pwrc);
            records.append((timestamp,cid,temp,tgood,pwr,random.gauss(POWER_LEVEL,1.0),
                        ctype,                # ContentType
                        o2,  # O2
                        co2, # CO2
                        tdoor, # Time_Door_Open
                        0,    # maintenance not required
                        random.randrange(DEFROST_LEVEL)))
        return records