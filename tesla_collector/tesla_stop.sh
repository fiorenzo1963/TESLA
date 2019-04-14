#!/bin/bash
pids=`ps auxw | grep tesla_collector | grep -v grep | awk '{print $2;}'`
if [ "$pids" != "" ]
then
	echo -n $0: kill -HUP $pids
	kill -HUP $pids > /dev/null 2>&1
	echo -n . ; sleep 1
	echo -n . ; sleep 1
	echo -n . ; sleep 1
	echo ''
fi
pids=`ps auxw | grep tesla_collector | grep -v grep | awk '{print $2;}'`
if [ "$pids" != "" ]
then
	echo -n $0: kill -KILL $pids
	kill -HUP $pids > /dev/null 2>&1
	echo -n . ; sleep 1
	echo -n . ; sleep 1
	echo -n . ; sleep 1
	echo ''
fi
rm -f /var/lock/tesla_collector
rm -f /run/lock/tesla_collector
sleep 1
