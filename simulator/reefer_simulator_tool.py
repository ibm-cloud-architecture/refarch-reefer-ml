import csv, sys, json, datetime
import random
import numpy as np
import pandas as pd
import os
import ReeferSimulator from reefer_simulator

'''
Tool to create the csv file for ML work using the Reefer metrics simulator.
'''

FILENAME = "../testdata"

def saveFile(df,fname = FILENAME,flag = "yes"):
    print("Save to file ", fname)  
    #df.to_csv(fname, sep=',')  
    if not os.path.isfile(fname):
        df.to_csv(fname, sep=',')
    elif flag == "no" or flag == "n":
        df.to_csv(fname, sep=',')
    else: # else it exists so append without writing the header
        df.to_csv(fname, sep=',', mode='a', header=False)
    #df.to_csv(fname, sep=',',mode='a', header=None)
    

def parseArguments():
    nb_records = 1000
    tgood = 4.4
    fname = "testdata"
    flag = "yes"
    cid = 101
    if len(sys.argv) == 1:
        print("Usage reefer_simulator --stype [poweroff | co2sensor | atsea]")
        print("\t --cid <container ID>")
        print("\t --records <the number of records to generate>")
        print("\t --temp <expected temperature for the goods>")
        print("\t --file <the filename to create (without .csv)>")
        print("\t --append [yes | no]")
        exit(1)
    else:
        for idx in range(1, len(sys.argv)):
            arg=sys.argv[idx]
            if arg == "--stype":
                simulation_type = sys.argv[idx + 1]
            elif arg == "--cid":
                cid = sys.argv[idx + 1]
            elif arg == "--records":
                nb_records = sys.argv[idx + 1]
            elif arg == "--temp":
                tgood = int(sys.argv[idx + 1])
            elif arg == "--file":
                fname = sys.argv[idx + 1]
            elif arg == "--append":
                flag = sys.argv[idx + 1]
    return (cid, simulation_type, nb_records, tgood, fname,flag)




if __name__ == "__main__":
    (cid, simulation_type, nb_records, tgood, fname,flag) = parseArguments()
    print(cid, simulation_type, nb_records, tgood, fname,flag)
    simulator = ReeferSimulator()
    if simulation_type == POWEROFF_SIMUL:
        df=simulator.generatePowerOff(cid,nb_records,tgood)
    elif  simulation_type == CO2_SIMUL:
        df=simulator.generateCo2(cid,nb_records,tgood)
    else:
        print("Not a valid simulation")
        exit 
    saveFile(df,fname,flag)