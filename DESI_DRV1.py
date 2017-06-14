#!/usr/bin/python
# @Author: Eddie Ruano
# @Date:   2017-05-01 05:14:54
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-02 13:00:36

"""
Basic DESI Driver for Prototyping
"""
import sys
import os.path
import time
# Customs Mods #
import Adafruit_MPR121.MPR121 as MPR121
import RPi.GPIO as GPIO
# Local Modules #
### Set path ###
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import drivers.VoyagerHCSR04 as VoyagerHCSR04

# #Buttons# #
G_INSTART = 9
G_INPAUSE= 10
G_INSTOP = 11
G_INSLOW = 5
G_INMED = 6
G_INFAST = 13
G_INFASTER = 19
G_INFASTEST = 26
# #Relays# #
GR_START = 14
GR_PAUSE = 18
GR_OFF = 15
GR_ENTER = 23
# #Keypad Relays# #
GR_00 = 24
GR_01 = 25
GR_02 = 8
GR_03 = 7
GR_04 = 12
GR_05 = 16
GR_ALEXA = 21
# #BOUNCE IN MS# #
bounceTime = 800
# #STATE# #
state = "Startup"
### MAIN PROGRAM START ###
def main():
   GPIO.setmode(GPIO.BCM)
   initializeButtons(G_INSTART, G_INPAUSE)
   initializeKnob(G_INSTOP, G_INSLOW, G_INMED, G_INFAST, G_INFASTER, G_INFASTEST)
   initializeRelay(GR_START, GR_OFF, GR_PAUSE, GR_ENTER, GR_00, GR_01, GR_02, GR_03, GR_05, GR_ALEXA) 

   GPIO.add_event_detect(G_INSTART, GPIO.FALLING, performStart, bounceTime)
   GPIO.add_event_detect(G_INPAUSE, GPIO.FALLING, performStop, bounceTime)
   GPIO.add_event_detect(G_INSTOP, GPIO.FALLING, performS0, bounceTime)
   GPIO.add_event_detect(G_INSLOW, GPIO.FALLING, performS1, bounceTime)
   GPIO.add_event_detect(G_INMED, GPIO.FALLING, performS2, bounceTime)
   GPIO.add_event_detect(G_INFAST, GPIO.FALLING, performS3, bounceTime)
   GPIO.add_event_detect(G_INFASTER, GPIO.FALLING, performS4, bounceTime)

   activeFlag = True
   print("In Main Loop:\n")
   while activeFlag:
        try:
            if state != "Shutdown":
                activeFlag = True
            else:
                print("Cleaning GPIO..")
                GPIO.cleanup()
                sys.exit(1)
        # Catch Ctrl+C
        except KeyboardInterrupt:
            GPIO.cleanup()
            sys.exit(0)
            print("Shutdown Mission.")
            #Should not get here
def performS0(channel):
   global state
   if state != "Startup" and state != "Speed0":
      # Trigger 0 twice
      GPIO.output(GR_00, GPIO.LOW)
      time.sleep(0.1)
      GPIO.output(GR_00, GPIO.HIGH)
      time.sleep(0.1)
      GPIO.output(GR_00, GPIO.LOW)
      time.sleep(0.1)
      GPIO.output(GR_00, GPIO.HIGH)
      time.sleep(0.1)
      #enter
      GPIO.output(GR_ENTER, GPIO.LOW)
      time.sleep(0.1)
      GPIO.output(GR_ENTER, GPIO.HIGH)
      time.sleep(0.1)
      global state
      state = "Speed0"
      print(state)
def performS1(channel):
   global state
   if state != "Speed1":
      # Trigger 1 twice
      GPIO.output(GR_01, GPIO.LOW)
      time.sleep(0.1)
      GPIO.output(GR_01, GPIO.HIGH)
      time.sleep(0.1)
      GPIO.output(GR_05, GPIO.LOW)
      time.sleep(0.1)
      GPIO.output(GR_05, GPIO.HIGH)
      time.sleep(0.1)
      #enter
      GPIO.output(GR_ENTER, GPIO.LOW)
      time.sleep(0.1)
      GPIO.output(GR_ENTER, GPIO.HIGH)
      time.sleep(0.1)
      global state
      state = "Speed1"
      print(state)
def performS2(channel):
   global state
   if state != "Speed2":
      # Trigger 1 twice
      GPIO.output(GR_02, GPIO.LOW)
      time.sleep(0.1)
      GPIO.output(GR_02, GPIO.HIGH)
      time.sleep(0.1)
      GPIO.output(GR_05, GPIO.LOW)
      time.sleep(0.1)
      GPIO.output(GR_05, GPIO.HIGH)
      time.sleep(0.1)
      #enter
      GPIO.output(GR_ENTER, GPIO.LOW)
      time.sleep(0.1)
      GPIO.output(GR_ENTER, GPIO.HIGH)
      time.sleep(0.1)
      #state variable
      global state
      state = "Speed2"
      print(state)
def performS3(channel):
   global state
   if state != "Speed3":
      # Trigger 1 twice
      GPIO.output(GR_03, GPIO.LOW)
      time.sleep(0.1)
      GPIO.output(GR_03, GPIO.HIGH)
      time.sleep(0.1)
      GPIO.output(GR_00, GPIO.LOW)
      time.sleep(0.1)
      GPIO.output(GR_00, GPIO.HIGH)
      time.sleep(0.1)
      #enter
      GPIO.output(GR_ENTER, GPIO.LOW)
      time.sleep(0.1)
      GPIO.output(GR_ENTER, GPIO.HIGH)
      time.sleep(0.1)
      #state variable
      global state
      state = "Speed3"
      print(state)
def performS4(channel):
   global state
   if state != "Speed4":
      # Trigger 1 twice
      GPIO.output(GR_03, GPIO.LOW)
      time.sleep(0.1)
      GPIO.output(GR_03, GPIO.HIGH)
      time.sleep(0.1)
      GPIO.output(GR_05, GPIO.LOW)
      time.sleep(0.1)
      GPIO.output(GR_05, GPIO.HIGH)
      time.sleep(0.1)
      #enter
      GPIO.output(GR_ENTER, GPIO.LOW)
      time.sleep(0.1)
      GPIO.output(GR_ENTER, GPIO.HIGH)
      time.sleep(0.1)
      global state
      state = "Speed4"
      print(state)
def performStart(self):
   if state == "Startup":
      print("start")
      GPIO.output(GR_START, GPIO.LOW)
      time.sleep(0.1)
      GPIO.output(GR_START, GPIO.HIGH)
      time.sleep(0.1)
      GPIO.output(GR_ENTER, GPIO.LOW)
      time.sleep(0.1)
      GPIO.output(GR_ENTER, GPIO.HIGH)
      time.sleep(0.1)
      performS0(channel)
   else:
      print("Already Started.")

def performStop(channel):
   global state
   if state == "Speed0":
      print("Shutting Down.")
      GPIO.output(GR_OFF, GPIO.LOW)
      time.sleep(0.1)
      GPIO.output(GR_OFF, GPIO.HIGH)
      time.sleep(0.1)
      global state
      state = "Shutdown"
      print(state)
   else:
      print("Pausing...\n")
      GPIO.output(GR_PAUSE, GPIO.LOW)
      time.sleep(0.1)
      GPIO.output(GR_PAUSE, GPIO.HIGH)
      time.sleep(0.1)
      state = "Paused"
      print(state)
def initializeButtons(start, pause):
   GPIO.setup(start, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   GPIO.setup(pause, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   print("Buttons Complete.")
   print("Start & Pause Set.\n")
def initializeKnob(speed0, speed1, speed2, speed3, speed4, speed5):
   GPIO.setup(speed0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   GPIO.setup(speed1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   GPIO.setup(speed2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   GPIO.setup(speed3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   GPIO.setup(speed4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   GPIO.setup(speed5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   print("Knob Complete.\n")
def initializeRelay(start, off, pause, enter, k0, k1, k2, k3, k5, alexa):
   GPIO.setup(start, GPIO.OUT)
   GPIO.setup(off, GPIO.OUT)
   GPIO.setup(pause, GPIO.OUT)
   GPIO.setup(enter, GPIO.OUT)
   GPIO.setup(k0, GPIO.OUT)
   GPIO.setup(k1, GPIO.OUT)
   GPIO.setup(k2, GPIO.OUT)
   GPIO.setup(k3, GPIO.OUT)
   GPIO.setup(k5, GPIO.OUT)
   GPIO.setup(alexa, GPIO.OUT)
   GPIO.output(start, GPIO.HIGH)
   GPIO.output(off, GPIO.HIGH)
   GPIO.output(pause, GPIO.HIGH)
   GPIO.output(enter, GPIO.HIGH)
   GPIO.output(k0, GPIO.HIGH)
   GPIO.output(k1, GPIO.HIGH)
   GPIO.output(k2, GPIO.HIGH)
   GPIO.output(k3, GPIO.HIGH)
   GPIO.output(k5, GPIO.HIGH)
   GPIO.output(alexa, GPIO.HIGH)
   print("Relays Complete.\n")
###MAIN CALL ###
if __name__ == "__main__":
   main()
