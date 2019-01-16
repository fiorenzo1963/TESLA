#!/bin/bash
echo -n $0:
killall -HUP tesla_collector.py > /dev/null 2>&1
echo -n . ; sleep 1
echo -n . ; sleep 1
killall -KILL tesla_collector.py > /dev/null 2>&1
echo -n . ; sleep 1
echo -n . ; sleep 1
rm -f /var/lock/tesla_collector
rm -f /run/lock/tesla_collector
echo ''
./tesla_collector.py
