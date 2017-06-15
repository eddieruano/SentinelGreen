#!/bin/bash
echo "Starting"
cd ~/Desktop/SentinelGreen
git pull
echo "Pulling"
[ -f on.dat ] || sudo python3 MissionControl.py
