#!/usr/bin/python3

import os
import sys
import json
from teslaapi import Connection
from teslaapi import Vehicle

def main():
        _c = Connection()
        #print("c = " + str(_c))
        _v = Vehicle(_c)
        #print("v = " + str(_v))
        if len(sys.argv) == 1:
                cmd = "vehicles"
        else:
                cmd = sys.argv[1]
        #print("cmd = " + cmd)
        vehicles = _v.vehicles()
        #print("vehicles = " + str(vehicles))
        vehicle = vehicles['response'][0]
        #print("vehicle = " + str(vehicle))
        #print("vehicle = " + json.dumps(vehicle))
        id_s = vehicles['response'][0]['id_s']
        #print(sys.argv[0] + ": using first vehicle id = " + id_s)
        _v.set_vehicle_id(id_s)
        if cmd == "vehicles":
                print(json.dumps(vehicles, indent = 8))
                sys.exit(0)
        if cmd == "vehicle":
                print(json.dumps(vehicle, indent = 8))
                sys.exit(0)
        if cmd == "wakeup":
                print("sending wakeup command")
                _v.wake_up()
                sys.exit(0)
        if cmd == "data":
                data = _v.data()
                #print("data = " + str(data))
                print(json.dumps(data, indent = 8))
                sys.exit(0)
        print(sys.argv[0] + ": usage: " + sys.argv[0] + " vehicles|vehicle|wakeup|data")
        sys.exit(1)

main()
