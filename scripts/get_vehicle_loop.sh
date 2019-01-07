#!/bin/bash
while true
do
	echo -n ========================================== `date`
	./get_vehicle_info.sh charge
	./get_vehicle_info.sh drive
	sleep 5
done
