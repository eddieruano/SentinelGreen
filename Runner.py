# -*- coding: utf-8 -*-
# @Author: Eddie Ruano
# @Date:   2017-06-14 12:51:23
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-14 13:24:29
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
        data = {'Status': 'ON'}
        with open(self.outfile, 'w') as outfile:
            json.dump(data, outfile)
    def writeShutdownLock(self):
        data = {'Status': 'OFF'}
        with open(self.outfile, 'w') as outfile:
            json.dump(data, outfile)
    def writeSpeed(self, speed):
        data = {'Speed': speed.toString()}
        with open(self.outfile, 'w') as speedfile:
            json.dump(data, speedfile)