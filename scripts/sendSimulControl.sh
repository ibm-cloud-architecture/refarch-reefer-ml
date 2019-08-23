#!/bin/bash

if [[ $# -ne 2 ]];then
    echo "Usage: Need two arguments:  sendSimulControl.sh hostname simultype (co2sensor | poweroff)"
    exit
else
    hostn=$1
    stype=$2
fi

fname=$PWD/simulControl.json
# hostn=order-producer-python-reefer-shipment-solution.greencluster-fa9ee67c9ab6a7791435450358e564cc-0001.us-east.containers.appdomain.cloud
# orderwebaproute-reefershipmentsolution.apps.green-with-envy.ocp.csplab.local

url="http://$hostn/control"

echo ""
echo "Send $fname to $url"
sed "s/co2sensor/${stype}/g" $fname > new.json

curl -v  -H "accept: */*" -H "Content-Type: application/json" -d @$fname $url
rm new.json