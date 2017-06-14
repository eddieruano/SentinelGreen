#!/usr/bin/python
# @Author: Eddie Ruano
# @Date:   2017-05-01 05:14:54
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-04 21:19:14

"""
    DESI uses two HCSR04 proximity sensors to determine Megan's postition on the treadmill.
"""
# Libraries
import RPi.GPIO as GPIO
import time
 
class Voyager(object):
    StartTime = 0.0
    StopTime = 0.0
    TimeElapsed = 0.0
    """ Begin VoyagerHCSR04 class structure """
    def __init__(self, name, t_pin, e_pin):
        self.name = name
        self.trigger_pin = t_pin
        self.echo_pin = e_pin
        self.status = "Pass"

    def update_status(self, stat):
        self.status = stat
        return self.status

    def self_check(self):
        if self.get_distance() != -1:
            self.status = "Pass"
            return True
        else:
            self.status = "Fail"
            return False
    def get_distance(self):
        # Set Trigger to HIGH
        GPIO.output(self.trigger_pin, True)
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)
        # Create holders for times
        self.StartTime = time.time()
        # save StartTime
        self.TimeElapsed = self.StartTime
        while GPIO.input(self.echo_pin) == 0:
            self.StartTime = time.time()
            # if it goes too long
            if self.StartTime > (self.TimeElapsed + 0.1):
                print("oops")
                return(-1.0)
        # save time of arrival
        while GPIO.input(self.echo_pin) == 1:
            self.StopTime = time.time()
        # time difference between start and arrival
        self.TimeElapsed = self.StopTime - self.StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        self.distance = (self.TimeElapsed * 34300) / 2
        return self.distance