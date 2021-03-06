#!/usr/bin/python
# @Author: Eddie Ruano
# @Date:   2017-05-01 05:14:54
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-21 23:18:26
# 
"""
    MissionControl.py is a debugging tool for DESI_Sentinel
"""
################################## IMPORTS ###################################
import json
import logging
import os
import os.path
import signal
import subprocess
import sys
import time
from subprocess import check_output
#
from math import floor
# Customs Mods #
import RPi.GPIO as GPIO
import Sentinel as Sentinel
import Pusher as Pusher
# Local Modules #
################################### PATHS #####################################
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import DESIConfig as DESIConfig
import Runner as Runner
import drivers.MPR121 as MPR121
import drivers.VoyagerHCSR04 as VoyagerHCSR04
#import trigger.snowboydetect as snowboydetect
# Logging
LogLevel = logging.DEBUG        ## Change this later
LogLocation = "Logs/DESIRun.txt"
#-------S8Proto
# Create Instance of Logger
Houston = logging.getLogger(__name__)
# Setting Logging Level --Change from Debug later
Houston.setLevel(level=LogLevel)
# Set up Format Protocol --> Type of Msg, Name of Module, Time, PayloadMessage
HouForm = logging.Formatter('%(levelname)s:%(name)s:%(asctime)s:%(message)s')
# Set up File Handler + Add level + add formatter
HouFile = logging.FileHandler(LogLocation)
HouFile.setLevel(LogLevel)
HouFile.setFormatter(HouForm)
# Set up Stream Handler + level + format
HouStream = logging.StreamHandler()
HouStream.setLevel(LogLevel)
HouStream.setFormatter(HouForm)
# Add all handlers to instance of Handler
Houston.addHandler(HouStream)
Houston.addHandler(HouFile)
Houston.info("MissionControl Logger has been created.")
############################ INITIALIZE CLASSES ###############################
DESI = DESIConfig.DESI()
Voyager1 = VoyagerHCSR04.Voyager("Voyager1", DESI.PROX1_TRIG, DESI.PROX1_ECHO)
Voyager2 = VoyagerHCSR04.Voyager("Voyager2", DESI.PROX2_TRIG, DESI.PROX2_ECHO)
TouchSense = MPR121.MPR121()
Sentinel = Sentinel.Sentinel()
Runner = Runner.Runner("Runner1", "Status.json", "Speed.json", "Pid.json")
Pusher = Pusher.Pusher("MainPusher")
################################## PATHS ######################################
def main():
    global Houston
    # Variables/Flags
    jdata = open("Status.json")
    data = json.load(jdata)
    Houston.info(data)
    Runner.writeStartLock()
    pid = os.getpid()
    Runner.writePid(pid)
    flagRailWarning = False
    flagSelectorWarning = False
    flagProximityWarning = False
    flagRedux = False
    flagStartSet = False
    # Initialize DESI States
    DESI.initDESI()
    # Initialize Voyager Proximity Sensors
    DESI.initProximity(Voyager1, Voyager2)
    # Test the function:    
    thisTime = time.time()
    Pusher.pushMessage("DESI Alert Service", "Workout has begun at " + str(thisTime))
    try:
        if not TouchSense.begin():  # Init TouchSense Capacitive Sensor Array
            Houston.error("TouchSense failed to Start.")
            sys.exit(1)
    except OSError as e:
        print(e)
        Houston.error("TouchSense failed to Start/caused OSError")
        sys.exit(1)
    Sentinel.getStateKnob(DESI)
    Sentinel.setStateKnob()
    time.sleep(1)
    Sentinel.getStateKnob(DESI)
    Sentinel.setStateKnob()
    Sentinel.updateActiveLock(TouchSense)
    # Single Start Trigger
    GPIO.add_event_detect(DESI.IN_START, GPIO.FALLING, callback=StartHandler, bouncetime=Sentinel.CONST_BOUNCE)
    try:
        Houston.info("Listen Try Begin.")
        #Wait for the Start Command
        Houston.info("Waiting for start.")
        while not Sentinel.StartDetect:
            Sentinel.getStateKnob(DESI)
            Sentinel.setStateKnob()
        #Wait until the correct Knob State Happens
        Houston.info("Waiting for knob")
        print(Sentinel.StateKnob)
        while Sentinel.StateKnob != 0.0:
            # if the counter reaches zero issue warning
            if (Sentinel.SpCount == 0):
                DESI.DESISendResponse("audio/wav_sp_sel.wav")
                Sentinel.SpCount = Sentinel.CONST_RESCOUNT
            else:
                # decrement counter
                time.sleep(0.1)
                Sentinel.SpCount-=1
            # we verify here
            Sentinel.getStateKnob(DESI)
            Sentinel.setStateKnob()
        # in correct setting so we wait for speech mutex
        Sentinel.waitMutexSpeech()
        DESI.DESISendResponse("audio/wav_okay_megan.wav")
        # issue start
        Sentinel.waitMutexSpeech()
        DESI.DESISendResponse("audio/wav_lets_start.wav")
        # officially add pause event
        GPIO.add_event_detect(DESI.IN_PAUSE, GPIO.FALLING, callback=PauseHandler, bouncetime=Sentinel.CONST_BOUNCE)
        flagStartSet = True

        while True:
            if Sentinel.flagShut == True:
                Houston.info("Shutdown. Loop.")
                break
            localKnobState = Sentinel.StateKnob
            # Update the ActiveLock
            Sentinel.updateActiveLock(TouchSense)
            # Query the knob states
            Sentinel.getStateKnob(DESI)
            # Set the Knob State according to the recent get
            Sentinel.setStateKnob()
            speed = getSpeed()
            if (Sentinel.StateKnob == 0.0) and (flagStartSet == False):
                GPIO.add_event_detect(DESI.IN_START, GPIO.FALLING, callback=StartHandler, bouncetime=Sentinel.CONST_BOUNCE)
                flagStartSet = True
            elif(flagStartSet == True):
                GPIO.remove_event_detect(DESI.IN_START)
                flagStartSet = False
                
            # Check if the knob changed position
            if (Sentinel.StateKnob != localKnobState):
                localKnobState = Sentinel.StateKnob
                speed = getSpeed()
                if Sentinel.flagPause == False:
                    DESI.DESISend(speed)
                Houston.debug("StateIdiff")
                print(speed)
            if (Sentinel.CapLock == True):
                Runner.writeSpeed(0.0, DESI)
                continue
            if (Sentinel.ProxLock == True):
                Runner.writeSpeed(0.0, DESI)
                continue
            Runner.writeSpeed(speed, DESI)
            # Set the Speed if the knob doesn't match up
            #if (Sentinel.StateKnob != Sentinel.ActualSpeed):
            #    DESI.DESISend(Sentinel.StateKnob * 1.0)
            #    Sentinel.ActualSpeed = (speed)
            # Here we check for contact
            """ CAPACITANCE CHECKS """
            # Check for an issue warning
            flagRailWarning = checkRailWarning(flagRailWarning)
            # if we aren't touching
            if not Sentinel.ActiveLock and Sentinel.flagPause == False:
                Houston.error("NO CONTACT")
                # If we reach zero on the counter and not in pause
                if ((Sentinel.CapCountdown == 0) and (Sentinel.CapLock == False)):
                    # save current workout state
                    saved_state = Sentinel.StateKnob
                    Sentinel.waitMutexSpeech()
                    DESI.DESISendResponse(DESI.RespondLock)   #pause
                    DESI.DESISend("Pause")
                    Sentinel.flagPause = True
                    print(DESI.State_Main)
                    # Enable the CapLock
                    Sentinel.CapLock = True
                    Houston.info("CapLocked.")
                    # Runs forever until CapLock disabled
                else:
                    # Else we are not making contact but not end of count
                    Sentinel.CapCountdown -= 1
            else:  # we are making contact
                    Sentinel.CapCountdown = Sentinel.CAPCOUNT
                    flagRailWarning = False
            
            """ START PROXIMITY CHECKS """
            Sentinel.Proximity = queryDistance()
            #print (Sentinel.Proximity)
            if Sentinel.Proximity > 12.0 and Sentinel.flagPause == False:
                flagProximityWarning = True
                # If we reach zero on the counter and not in pause
                if ((Sentinel.ProxCountdown == 0) and (Sentinel.ProxLock == False)):
                    Sentinel.ProximityRetries += 1
                    # reduce speed
                    i = 0.0
                    while i < Sentinel.Redux:
                        #print("Reducing By: " + i)
                        DESI.DESISend("SendDown")
                        i += 1.0
                        flagRedux = True
                        Sentinel.ActualSpeed = Sentinel.ActualSpeed - 0.1
                    # Enable the CapLock
                    if (Sentinel.ProximityRetries > Sentinel.CONST_PROX_RETRIES):
                        Sentinel.ProxLock = True
                        DESI.DESISend("Pause")
                        Sentinel.flagPause = True
                        Sentinel.waitMutexSpeech()
                        DESI.DESISendResponse(DESI.RespondLock)
                        Houston.info("ProxLocked")
                    # Runs forever until CapLock disabled
                else:
                    # Else we are not making contact but not end of count
                    Sentinel.ProxCountdown -= 1
            else:  # we are making contact
                    Sentinel.ProxCountdown = Sentinel.PROXCOUNT
                    flagProximityWarning = False
                    sp = getSpeed()
                    if flagRedux:
                        DESI.DESISend(sp)
                        flagRedux = False
            """"""""""""" END PROXIMITY CHECKS """""""""""""""""""""
            #print(Sentinel.ActualSpeed)
            time.sleep(Sentinel.RunningLoopSpeed)
    except KeyboardInterrupt:
        Houston.info("Shutdown Mission By SuperVisor.")
    finally: 
        GPIO.cleanup()
        DESI.DESICleanup()
        try:
            Runner.writeShutdownLock()
        except:
            Houston.info("Tried to delete ON.dat but it was gone.")
        Houston.info("Finally Shutdown Mission.")
        sys.exit(0)
        #Detector.terminate()
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
    distv1 = sanitizeDistance(Voyager1, distv1)
    distv2 = sanitizeDistance(Voyager2, distv2)
    # Subtract 3.5 to get 0
    distv1 = abs(distv1 - 3.5)
    distv2 = abs(distv2 - 3.5)
    if distv1 == -1.0 and distv2 != -1.0:
        print("Check Sensor 1")
        return distv2
    elif distv2 == -1.0 and distv1 != -1.0:
        print("Check Sensor 2")
        return distv1
    else:
        ave = (distv1 + distv2) / 2
    return ave
def sanitizeDistance(voy, inDist):
    tries = 0
    while inDist == -1.0 and tries < Sentinel.ProximityRetries:
        inDist = Voyager1.get_distance()
    return inDist
def StartHandler(channel):
    global Houston
    global Runner
    global Sentinel
    global DESI
    if (Sentinel.StateKnob == 0.0) and DESI.State_Main == "Pause":
        DESI.DESISend("Shutdown")
        Sentinel.flagShut = True
        GPIO.cleanup()
        DESI.DESICleanup()
        Houston.info("StartHandler: Shutdown")
        try:
            Runner.writeShutdownLock()
        except:
            restart()
            Houston.info("Tried to delete ON.dat but it was gone.")
        sys.exit(0)
    elif Sentinel.StartDetect != True:
        Houston.info("StartHandler: Startup")
        Sentinel.StartDetect = True
        DESI.DESISend("Start")
    else:
        pass
def getSpeed():
    global Sentinel
    if Sentinel.StateKnob == 0.0:
        Sentinel.setSpeed(0.0)
        return "Send00"
    elif Sentinel.StateKnob == 1.0:
        Sentinel.setSpeed(2.0)
        return "Send01"
    elif Sentinel.StateKnob == 2.0:
        Sentinel.setSpeed(2.5)
        return "Send02"
    elif Sentinel.StateKnob == 3.0:
        Sentinel.setSpeed(3.0)
        return "Send03"
    elif Sentinel.StateKnob == 4.0:
        Sentinel.setSpeed(3.5)
        return "Send04"
    else:
        return "Send00"
def PauseHandler(channel):
    global Houston
    global Sentinel
    global DESI
    Houston.info("PauseHandler: Pause Interrupt")
    DESI.DESISend("Pause")
    Sentinel.flagPause = not Sentinel.flagPause
    if Sentinel.CapLock == True:
        Sentinel.CapLock = False
    elif Sentinel.ProxLock == True:
        Sentinel.ProxLock = False
        Sentinel.ProximityRetries = 0
def checkRailWarning(flag):
    if ((Sentinel.ActiveLock == False) and (flag == False)):
        if (Sentinel.CapCountdown == (Sentinel.CAPCOUNT / 2)):
            DESI.DESISendResponse(DESI.RespondRails)
        return True
    return False
def restart():
    global Houston
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    Houston.info(output)
### MAIN CALL ###
if __name__ == "__main__":
    main()