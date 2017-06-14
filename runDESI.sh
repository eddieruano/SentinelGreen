#!/bin/bash
echo "Starting"
cd ~/Desktop/GreenSentinel
git pull
echo "Pulling"
[ -f on.dat ] || sudo python3 MissionControl.py
