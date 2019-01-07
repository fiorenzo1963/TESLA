#!/bin/bash
while true
do
	echo -n ========================================== `date`
	./get_vehicle_streaming.sh
	sleep 2
done
