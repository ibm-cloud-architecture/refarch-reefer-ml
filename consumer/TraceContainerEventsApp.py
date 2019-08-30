import os,sys
from ContainerEventsListener import ContainerEventsListener

CID="100"
def parseArguments():
    if len(sys.argv) != 2:
        print("Need to have at least one argument container ID")
        exit(1)
    CID = sys.argv[1]
    print("The arguments are: " , str(sys.argv))

if __name__ == '__main__':
    parseArguments()
    consumer = ContainerEventsListener()
    consumer.processEvents(CID)
    consumer.close()