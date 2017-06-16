# -*- coding: utf-8 -*-
# @Author: Eddie Ruano
# @Date:   2017-06-14 12:51:23
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-16 13:43:46
import os
import json
import datetime
import time
import string

class Runner(object):

    def __init__(self, name, outfile, speedfile):
        self.name = name
        self.outfile = outfile
        self.speedfile = speedfile
    def writeStartLock(self):
        file = open('ON.dat', 'w+')
        data = {'Status': 'ON'}
        with open(self.outfile, 'w') as outfile:
            json.dump(data, outfile)
    def writeShutdownLock(self):
        os.remove("ON.dat")
        data = {'Status': 'OFF'}
        with open(self.outfile, 'w') as outfile:
            json.dump(data, outfile)
    def writeSpeed(self, speed, desi):
        speed = self._translateToSpeed(speed)
        if (desi.State_Main == "Pause"):
            speed = 0.0
        data = {'Speed': str(speed)}
        with open(self.speedfile, 'w') as speedfile:
            json.dump(data, speedfile)
    def _translateToSpeed(self, speed):
        if speed == "Send00":
            return 0.0
        elif speed == "Send01":
            return 2.0
        elif speed == "Send02":
            return 2.5
        elif speed == "Send03":
            return 3.0
        elif speed == "Send04":
            return 3.5
        else:
            return 100.0