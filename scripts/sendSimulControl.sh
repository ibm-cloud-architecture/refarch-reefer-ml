#!/bin/bash

if [[ $# -ne 4 ]];then
    echo "Usage: Need four arguments:  sendSimulControl.sh hostname simultype (co2sensor | o2sensor | poweroff) containerID nb_of_records"
    echo "Let use default settings"
    # CSP one: 
    hostn="reefersimulatorroute-reefershipmentsolution.apps.green-with-envy.ocp.csplab.local"
    # IBMCLOUD one hostn="reefersimulatorroute-reefer-shipment-solution.greencluster-fa9ee67c9ab6a7791435450358e564cc-0001.us-east.containers.appdomain.cloud/"
    stype="co2sensor"
    cid="C01"
    nb_records=200
else
    hostn=$1
    stype=$2
    cid=$3
    nb_records=$4
fi

fname=$PWD/scripts/simulControl.json


url="http://$hostn/control"

echo ""
echo "Send $fname to $url"
sed "s/co2sensor/${stype}/g" $fname > new.json
if [[ $(uname) == "Darwin" ]] ; then
  sed -i '' "s/C02/${cid}/g" new.json
  sed -i '' "s/25/${nb_records}/g" new.json
else
  sed -i "s/C02/${cid}/g" new.json
  sed -i "s/25/${nb_records}/g" new.json
fi

echo "POST the following data:"
cat new.json
curl -v  -H "accept: */*" -H "Content-Type: application/json" -d @new.json $url
rm new.json
