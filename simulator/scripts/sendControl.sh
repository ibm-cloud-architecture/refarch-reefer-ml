#!/bin/bash

if [[ $# -ne 2 ]];then
    echo "Usage: Need two arguments:  createOrder.sh hostname anOrderID"
    exit
else
    hostn=$1
    oid=$2
fi

fname=$PWD/data/order1.json
# hostn=order-producer-python-reefer-shipment-solution.greencluster-fa9ee67c9ab6a7791435450358e564cc-0001.us-east.containers.appdomain.cloud
# orderwebaproute-reefershipmentsolution.apps.green-with-envy.ocp.csplab.local

url="http://$hostn/order"

echo ""
echo "Send $fname to $url"
sed "s/o01/${oid}/g" $fname > new.json

curl -v  -H "accept: */*" -H "Content-Type: application/json" -d @$fname $url
rm new.json