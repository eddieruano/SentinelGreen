# -*- coding: utf-8 -*-
# @Author: Eddie Ruano
# @Date:   2017-06-14 12:51:23
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-14 13:08:13
import json
import datetime
import time

class Runner(object):

    def __init__(self, name, outfile):
        self.name = name
        self.outfile = outfile
    def writeStartLock(self):
        data = {'Status': 'ON'}
        with open(self.outfile, 'w') as outfile:
            json.dump(data, outfile)
    def writeShutdownLock(self):
        data = {'Status': 'OFF'}
        with open(self.outfile, 'w') as outfile:
            json.dump(data, outfile)
    