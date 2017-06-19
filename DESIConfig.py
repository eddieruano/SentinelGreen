# -*- coding: utf-8 -*-
# @Author: Eddie Ruano
# @Date:   2017-06-01 07:23:39
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-19 11:59:15


import RPi.GPIO as GPIO
import time
import pyaudio
import wave
import subprocess
class DESI(object):
    # Logging
    LogLevel = logging.DEBUG        ## Change this later
    LogLocation = "Logs/DESIConfig.txt"
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
    Houston.info("DesiConfig Logger has been created.")
    """Representation of a DESI Entity"""
    # Control Box Pins
    SPEED0 = 0.0
    SPEED1 = 2.0
    SPEED2 = 2.5
    SPEED3 = 3.0
    SPEED4 = 3.5
    IN_START    = 9
    IN_PAUSE    = 10
    IN_SPEED0   = 11
    IN_SPEED1   = 5
    IN_SPEED2   = 6
    IN_SPEED3   = 13
    IN_SPEED4   = 19
    # Proximity Sensor Pins
    PROX1_TRIG  = 17
    PROX1_ECHO  = 4
    PROX2_TRIG  = 22
    PROX2_ECHO  = 27
    # Relay Pins
    OUT_START   = 14
    OUT_OFF     = 15
    OUT_PAUSE   = 18
    OUT_ENTER   = 23
    OUT_0       = 24
    OUT_1       = 25
    OUT_2       = 8
    OUT_3       = 7
    OUT_4       = 21
    OUT_5       = 16
    OUT_DOWN    = 12
    #OUT_ALEXA   = 20
    # States of DESI
    State_Main  = "Idle"
    State_Knob  = "Speed0"
    State_Touch = "Negative"
    State_Speed = 0.0

    Zone_Yellow = 10.0
    Zone_Red = 12.5
    Time_Bounce = 800
    # Audio
    RespondStart   = "audio/wav_lets_start.wav"
    RespondSpeed00 = "audio/wav_tspeed0.wav"
    RespondSpeed01 = "audio/wav_tspeed1.wav"
    RespondSpeed02 = "audio/wav_tspeed2.wav"
    RespondSpeed03 = "audio/wav_tspeed3.wav"
    RespondSpeed04 = "audio/wav_tspeed4.wav"
    RespondPause = "audio/wav_pause2.wav"
    RespondPaused = "audio/wav_paused.wav"
    RespondOkay = "audio/wav_okay_megan.wav"
    RespondRails = "audio/wav_rem_rails.wav"
    RespondProx = "audio/wav_rem_rails.wav"
    RespondRestart = "audio/wav_restart.wav"
    # Constructor
    def __init__(self):
        """Create an instance of DESI"""
        # Nothing to do here since there is very little state in the class.
        pass
    def initDESI(self):
        # Set up GPIO stuff
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False) #check
        self.initControlBox()
        self.initRelays()
    def initControlBox(self):
        GPIO.setup(self.IN_START, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.IN_PAUSE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.IN_SPEED0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.IN_SPEED1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.IN_SPEED2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.IN_SPEED3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.IN_SPEED4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.Houston.info("Buttons Complete.")
    def initProximity(self, sensorV1, sensorV2):
        # Set up the correct In/Out Scheme for send/receive
        GPIO.setup(sensorV1.trigger_pin, GPIO.OUT)
        GPIO.setup(sensorV1.echo_pin, GPIO.IN)
        GPIO.setup(sensorV2.trigger_pin, GPIO.OUT)
        GPIO.setup(sensorV2.echo_pin, GPIO.IN)
        self.Houston.info("Proximity Sensor Set.")
    def initRelays(self):
        # Set up the correct In/Out Scheme for send/receive
        GPIO.setup(self.OUT_START, GPIO.OUT)
        GPIO.setup(self.OUT_OFF, GPIO.OUT)
        GPIO.setup(self.OUT_PAUSE, GPIO.OUT)
        GPIO.setup(self.OUT_ENTER, GPIO.OUT)
        GPIO.setup(self.OUT_0, GPIO.OUT)
        GPIO.setup(self.OUT_1, GPIO.OUT)
        GPIO.setup(self.OUT_2, GPIO.OUT)
        GPIO.setup(self.OUT_3, GPIO.OUT)
        GPIO.setup(self.OUT_4, GPIO.OUT)
        GPIO.setup(self.OUT_5, GPIO.OUT)
        GPIO.setup(self.OUT_DOWN, GPIO.OUT)
        #GPIO.setup(self.OUT_ALEXA, GPIO.OUT)
        GPIO.output(self.OUT_START, GPIO.HIGH)
        GPIO.output(self.OUT_OFF, GPIO.HIGH)
        GPIO.output(self.OUT_PAUSE, GPIO.HIGH)
        GPIO.output(self.OUT_ENTER, GPIO.HIGH)
        GPIO.output(self.OUT_0, GPIO.HIGH)
        GPIO.output(self.OUT_1, GPIO.HIGH)
        GPIO.output(self.OUT_2, GPIO.HIGH)
        GPIO.output(self.OUT_3, GPIO.HIGH)
        GPIO.output(self.OUT_4, GPIO.HIGH)
        GPIO.output(self.OUT_5, GPIO.HIGH)
        GPIO.output(self.OUT_DOWN, GPIO.HIGH)
        #GPIO.output(self.OUT_ALEXA, GPIO.HIGH)
        self.Houston.info("Relay Array Set.")
    
    def DESISend(self, command):
        if command == "Start":
            self.performStart()
            self.Houston.info("SendStart")
        elif command == "Pause":
            self.performPause()
            #self.DESISendResponse(self.RespondPaused)
            self.Houston.info("SendPause")
        elif command == "Shutdown":
            self.DESICleanupAudio()
            #self.DESISendResponse(self.RespondShutdown)
            self.performShutdown()
            self.Houston.info("Shutdown")
        elif command == "Enter":
            self.performEnter()
            self.Houston.info("Enter")
        elif command == "Send00":
            self.DESICleanupAudio()
            self.DESISendResponse(self.RespondSpeed00)
            self.performS0()
            self.Houston.info("Send00")
        elif command == "Send01":
            self.DESICleanupAudio()
            self.DESISendResponse(self.RespondSpeed01)
            self.performS1()
            self.Houston.info("Send01")
        elif command == "Send02":
            self.DESICleanupAudio()
            self.DESISendResponse(self.RespondSpeed02)
            self.performS2()
            self.Houston.info("Send02")
        elif command == "Send03":
            self.DESICleanupAudio()
            self.DESISendResponse(self.RespondSpeed03)
            self.performS3()
            self.Houston.info("Send03")
        elif command == "Send04":
            self.DESICleanupAudio()
            self.DESISendResponse(self.RespondSpeed04)
            self.performS4()
            self.Houston.info("Send04")
        elif command == "SendDown":
            self.performDown()
            self.Houston.info("SendDown")
        elif command == "SendAlexa":
            self.performAlexa()
            self.Houston.info("Alexa")
        else:
            self.Houston.error("Error with Command Sent to ")
    def DESISendResponse(self, fname):
        """ 
            Callback plays a wave file.
            :param str fname: wave file name
            :return: None
        """
        audio_subprocess = subprocess.Popen(["aplay", fname])
        pass
    def DESIUpdateState(self, state):
        pass
    def performStart(self):
        #if self.State_Main == "Idle":
        GPIO.output(self.OUT_START, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.OUT_START, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.OUT_ENTER, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.OUT_ENTER, GPIO.HIGH)
        time.sleep(0.1)
        self.performS0()
        #elif self.State_Main == "Pause":
        #    print("Shutdown")
        #    self.performShutdown()
        #else:
        #    print("Already Started")
    def performShutdown(self):
        print("Shutting Down")
        #if self.State_Main == "Pause":
        GPIO.output(self.OUT_OFF, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.OUT_OFF, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.OUT_OFF, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.OUT_OFF, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.OUT_ENTER, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.OUT_ENTER, GPIO.HIGH)
        time.sleep(0.1)
        self.State_Main = "Shutdown"
        #else:
        #    print("Nope")
    def performPause(self):
        # if self.State_Main != "Pause":
        GPIO.output(self.OUT_PAUSE, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.OUT_PAUSE, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.OUT_ENTER, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.OUT_ENTER, GPIO.HIGH)
        time.sleep(0.1)
        self.State_Main = "Pause"
    
    def performS0(self):
        GPIO.output(self.OUT_0, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.OUT_0, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.OUT_0, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.OUT_0, GPIO.HIGH)
        time.sleep(0.1)
        #
        GPIO.output(self.OUT_ENTER, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.OUT_ENTER, GPIO.HIGH)
        time.sleep(0.1)
        self.State_Main = "Speed0"
        self.State_Speed = self.SPEED0
        time.sleep(0.1)
        # else:
            # print("Nope")
    def performS1(self):
        # if self.State_Main == "Speed0" or self.State_Main == "Speed2":
        GPIO.output(self.OUT_2, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.OUT_2, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.OUT_0, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.OUT_0, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.OUT_ENTER, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.OUT_ENTER, GPIO.HIGH)
        time.sleep(0.1)
        self.State_Main = "Speed1"
        self.State_Speed = self.SPEED1
        time.sleep(0.1)
    def performS2(self):
        GPIO.output(self.OUT_2, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.OUT_2, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.OUT_5, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.OUT_5, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.OUT_ENTER, GPIO.LOW)
        #
        time.sleep(0.1)
        GPIO.output(self.OUT_ENTER, GPIO.HIGH)
        time.sleep(0.1)
        self.State_Main = "Speed2"
        self.State_Speed = self.SPEED2
        time.sleep(0.1)
    def performS3(self):
        GPIO.output(self.OUT_3, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.OUT_3, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.OUT_0, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.OUT_0, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.OUT_ENTER, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.OUT_ENTER, GPIO.HIGH)
        time.sleep(0.1)
        self.State_Speed = self.SPEED3
        time.sleep(0.1)
    def performS4(self):
        GPIO.output(self.OUT_3, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.OUT_3, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.OUT_5, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.OUT_5, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.OUT_ENTER, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.OUT_ENTER, GPIO.HIGH)
        time.sleep(0.1)
        self.State_Main = "Speed4"
        self.State_Speed = self.SPEED4
        time.sleep(0.1)
    def performDown(self):
        GPIO.output(self.OUT_DOWN, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.OUT_DOWN, GPIO.HIGH)
        time.sleep(0.1)
        self.State_Speed -= 0.1
    def performAlexa(self):
        GPIO.output(self.OUT_ALEXA, GPIO.LOW)
        time.sleep(0.2)
        GPIO.output(self.OUT_ALEXA, GPIO.HIGH)
        time.sleep(0.2)
    def DESIQuerySpeed(self):
        return self.State_Speed
    def DESICleanup(self):
        self.DESICleanupAudio()
    def DESICleanupAudio(self):
        subprocess.call(['killall', 'aplay'])

