#!/bin/bash

if [[ $# -ne 1 ]];then
    echo "Usage: Need one argument:  sendReeferTelemetry.sh hostname"
    echo "Let use default settings"
    # CSP one: hostn="reefersimulatorroute-reefershipmentsolution.apps.green-with-envy.ocp.csplab.local/"
    hostn="localhost:8080"
else
    hostn=$1
fi

fname=$PWD/telemetry.json


url="http://$hostn/predict"

echo ""
echo "Send $fname to $url"
sed "s/co2sensor/${stype}/g" $fname > new.json

echo "POST the following data:"
cat new.json
curl -v  -H "accept: */*" -H "Content-Type: application/json" -d @new.json $url
rm new.json
