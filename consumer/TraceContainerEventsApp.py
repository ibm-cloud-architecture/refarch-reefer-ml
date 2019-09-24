import os,sys
from ContainerEventsListener import ContainerEventsListener

CID="C100"
def parseArguments():
    if len(sys.argv) == 2:
        CID = sys.argv[1]
    print("The arguments are: " , str(sys.argv))

if __name__ == '__main__':
    print("Containers listener just to trace the topic v0.0.1")
    consumer = ContainerEventsListener()
    consumer.processEvents()
    consumer.close()