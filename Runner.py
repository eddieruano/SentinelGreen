# -*- coding: utf-8 -*-
# @Author: Eddie Ruano
# @Date:   2017-06-14 12:51:23
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-14 18:17:09
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
        file = open('on.dat', 'w+')
        data = {'Status': 'ON'}
        with open(self.outfile, 'w') as outfile:
            json.dump(data, outfile)
    def writeShutdownLock(self):
        os.remove("on.dat")
        data = {'Status': 'OFF'}
        with open(self.outfile, 'w') as outfile:
            json.dump(data, outfile)
    def writeSpeed(self, speed):
        data = {'Speed': str(speed)}
        with open(self.speedfile, 'w') as speedfile:
            json.dump(data, speedfile)