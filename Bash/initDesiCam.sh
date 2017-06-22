#!/bin/bash       
# Purpose: 			This Script Runs the entire DESI Sentinel System. 
# Author: 			Eddie Ruano for Megan's Treadmill Team
# Organization: 	Cal Poly Senior Project Group #31
# ------------------------------------------------------
# Details:  1.) Script starts a secure tunnel with NGROK so that Sys 
# 				Admin (Eddie Ruano) is able to log in and push updates.
# 				2.) Script Starts an NGROK tunnel to port 80 of this in order
# 				to access 
# 			  

# Get the current time
current_time="$(date +'%c')"
DESI_CamLog=/home/pi/Desktop/SentinelGreen/Logs/DesiCam.txt
DESI_CamLogN=/home/pi/Desktop/SentinelGreen/Logs/DesiCamN.txt
echo "Starting NGROK DESICAM at $current_time" >> $DESI_CamLog
cd /home/pi/NGrokServer/
sleep 3
./ngrok http -subdomain=desicam 80 > $DESI_CamLogN