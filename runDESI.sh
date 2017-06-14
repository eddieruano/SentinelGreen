#!/bin/bash
echo "Starting"
cd ~/Desktop/Sentinel
git pull
echo "Pulling"
sudo python3 ~/Desktop/Sentinel/MissionControl.py
