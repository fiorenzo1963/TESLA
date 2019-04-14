#!/bin/bash
./tesla_stop.sh
echo $0: starting
./tesla_collector.py
ps auxw | grep tesla_collector | grep -v grep | awk '{print $2;}'
