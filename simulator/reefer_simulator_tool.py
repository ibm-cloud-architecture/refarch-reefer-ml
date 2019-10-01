import csv, sys, json, datetime
import random
import numpy as np
import pandas as pd
import os
from simulator.domain.reefer_simulator import ReeferSimulator
from simulator.infrastructure.ReeferRepository import ReeferRepository

'''
Tool to create the csv file for ML work using the Reefer metrics simulator.
'''
FILENAME = "../ml/data/testdata.csv"

def saveFile(df,fname = FILENAME,flag = True):
    print("Save to file ", fname)  
    if not os.path.isfile(fname):
        df.to_csv(fname, sep=',',index=False,header=True,columns=ReeferSimulator.COLUMN_NAMES)
    elif flag:  # append without writing the header and index
        df.to_csv(fname, sep=',', mode='a', header=False,index=False,columns=ReeferSimulator.COLUMN_NAMES)
    else: 
        df.to_csv(fname, sep=',',index=False,columns=ReeferSimulator.COLUMN_NAMES)

    
def saveToDB(df):
    print(df)
    repo = ReeferRepository()
    repo.connect()
    repo.addReeferTelemetries(df)
    

def parseArguments():
    nb_records = 1000
    fname = FILENAME
    append = False
    useDB = False
    cid = "C01"
    product_id = "P02"
    simulation_type = "normal"
    if len(sys.argv) == 1:
        print("Usage reefer_simulator --stype [poweroff | co2sensor | o2sensor | normal]")
        print("\t --cid [C01 | C02 | C03 | C04]")
        print("\t --product_id [ P01 | P02 | P03 | P04 ]")
        print("\t --records <the number of records to generate>")
        print("\t --file <the filename to create (without .csv)>")
        print("\t --append")
        print("\t --db")
        exit(1)
    else:
        for idx in range(1, len(sys.argv)):
            arg=sys.argv[idx]
            if arg == "--stype":
                simulation_type = sys.argv[idx + 1]
            elif arg == "--cid":
                cid = sys.argv[idx + 1]
            elif arg == "--records":
                nb_records = int(sys.argv[idx + 1])
            elif arg == "--product_id":
                product_id = sys.argv[idx + 1]
            elif arg == "--file":
                fname = sys.argv[idx + 1]
            elif arg == "--append":
                append = True
            elif arg == "--db":
                useDB = True
    return (cid, simulation_type, nb_records, product_id, fname, append, useDB)


if __name__ == "__main__":
    (cid, simulation_type, nb_records, product_id, fname,append, useDB) = parseArguments()
    if useDB:
        print(cid, simulation_type, nb_records, product_id)
    else:
        print(cid, simulation_type, nb_records, product_id, fname, append)
    simulator = ReeferSimulator()
    if simulation_type == ReeferSimulator.SIMUL_POWEROFF:
        df=simulator.generatePowerOffRecords(cid,nb_records,product_id)
    elif  simulation_type == ReeferSimulator.SIMUL_CO2:
        df=simulator.generateCo2Records(cid,nb_records,product_id)
    elif  simulation_type == ReeferSimulator.SIMUL_O2:
        df=simulator.generateO2Records(cid,nb_records,product_id)
    elif  simulation_type == ReeferSimulator.NORMAL:
        df=simulator.generateNormalRecords(cid,nb_records,product_id)
    else:
        print("Not a valid simulation")
        exit 
    if (not useDB):
        saveFile(df,fname,append)
    else:
        saveToDB(df)