#!/bin/bash
echo "Starting" > Logs/RunDESI.txt
cd ~/Desktop/SentinelGreen
git pull
echo "Pulling" > Logs/RunDESI.txt
echo "Starting the Maid" > Logs/RunDESI.txt
sudo python3 StartMaid.py
echo "Starting Infinite Loop" > Logs/RunDESI.txt
while [ true ]; do
 [ -f on.dat ] || sudo python3 MissionControl.py
 sleep 40
done

