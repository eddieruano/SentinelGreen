#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Eddie Ruano
# @Date:   2017-06-21 22:27:41
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-21 23:11:07
import requests
import json

class Pusher(object):

    API_KEY = 'o.Nej9veaxrIJNTTcHFUDCuugm8ZsgxZYv'

    def __init__(self, name):
        self.name = name        

    # Send a message to all your registered devices.
    def pushMessage(title, body):
        data = {
            'type':'note', 
            'title':title,
            'body':body
        }
        resp = requests.post('https://api.pushbullet.com/api/pushes',data=data, auth=(API_KEY,''))