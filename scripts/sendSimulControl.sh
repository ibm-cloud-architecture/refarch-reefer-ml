#!/bin/bash

if [[ $# -ne 2 ]];then
    echo "Usage: Need two arguments:  sendSimulControl.sh hostname simultype (co2sensor | poweroff)"
    echo "Let use default settings"
    hostn="reefersimulatorroute-reefershipmentsolution.apps.green-with-envy.ocp.csplab.local/"
    stype="co2sensor"
else
    hostn=$1
    stype=$2
fi

fname=$PWD/simulControl.json


url="http://$hostn/control"

echo ""
echo "Send $fname to $url"
sed "s/co2sensor/${stype}/g" $fname > new.json

echo "POST the following data:"
cat new.json
curl -v  -H "accept: */*" -H "Content-Type: application/json" -d @new.json $url
rm new.json
