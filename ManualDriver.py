#!/usr/bin/python
# @Author: Eddie Ruano
# @Date:   2017-05-01 05:14:54
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-06 06:30:06
# 
"""
    MissionControl.py is a debugging tool for DESI_Sentinel
"""
### IMPORT MODULES ###
import sys
import os.path
import signal
import collections
import pyaudio
import wave
import time
# Customs Mods #
#import Adafruit_MPR121.MPR121 as MPR121
import RPi.GPIO as GPIO
# Local Modules #
### Set path ###
#sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
#import drivers.VoyagerHCSR04 as VoyagerHCSR04
import DESIConfig as DESIConfig
### Global Variables ###
DESI = DESIConfig.DESI()
#Voyager1 = VoyagerHCSR04.Voyager("Voyager1", DESI.PROX1_TRIG, DESI.PROX1_ECHO)
#Voyager2 = VoyagerHCSR04.Voyager("Voyager2", DESI.PROX2_TRIG, DESI.PROX2_ECHO)
#TouchSense = MPR121.MPR121()

def main():
    # Variables
    proxError = 0.0
    distv1 = 0.0
    distv2 = 0.0
    slack = 0.0
    contact = False
    ave = 0.0
    # Initialize DESI States
    DESI.initDESI()
    # Initialize Voyager Proximity Sensors
    #DESI.initProximity(Voyager1, Voyager2)
    # if not TouchSense.begin():  # Init TouchSense Capacitive Sensor Array
    #     print("TSense")
    #     sys.exit(1)
    try:
        print("Listening")
        #DESI.DESIListen()
        activeFlag = True
        while activeFlag == True:
            activeFlag = True
            command = input("Enter a command: ")
            if command == "start":
                DESI.DESISend("Start")
            elif command == "shutdown":
                DESI.DESISend("Shutdown")
            elif command == "pause":
                DESI.DESISend("Pause")
            elif command == "unpause":
                DESI.DESISend("Pause")
            elif command == "enter":
                DESI.DESISend("Enter")
            elif command == "0":
                DESI.DESISend("Send00")
            elif command == "1":
                DESI.DESISend("Send01")
            elif command == "2":
                DESI.DESISend("Send02")
            elif command == "3":
                DESI.DESISend("Send03")
            elif command == "4":
                DESI.DESISend("Send04")
            elif command == "down":
                DESI.DESISend("SendDown")
            elif command == "alexa":
                DESI.DESISend("SendAlexa")
            else:
                print("Invalid Command")
            print(DESI.State_Main)
            # Query for the proximity of Megan #       
            time.sleep(0.2)
    # Catch Ctrl+C
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Shutdown Mission.")
### END OF MAIN ###
"""Helper Functions"""
def activateAlexa():
    GPIO.output(DESI.OUT_ALEXA, GPIO.LOW)
    time.sleep(2)
    GPIO.output(DESI.OUT_ALEXA, GPIO.HIGH)
def queryDistance():
    distv1 = Voyager1.get_distance()
    distv2 = Voyager2.get_distance()
    # Sanitize
    distv1 = distv1 - 3.5
    distv2 = distv2 - 3.5
    print(distv1)
    print(distv2)
    ave = (distv1 + distv2) / 2
    return ave
### MAIN CALL ###
if __name__ == "__main__":
    main()