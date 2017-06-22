#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Eddie Ruano
# @Date:   2017-06-21 22:27:41
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-21 22:30:24
import requests
import json

API_KEY = 'o.Nej9veaxrIJNTTcHFUDCuugm8ZsgxZYv'

# Send a message to all your registered devices.
def pushMessage(title, body):
    data = {
        'type':'note', 
        'title':title,
        'body':body
        }
    resp = requests.post('https://api.pushbullet.com/api/pushes',data=data, auth=(API_KEY,''))

# Test the function:    
pushMessage("DESI/Sentinel Service", "DESI failed to sense Megan. If you would like to take a look, click this link: ")