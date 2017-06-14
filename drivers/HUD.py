# -*- coding: utf-8 -*-
# @Author: Eddie Ruano
# @Date:   2017-06-01 12:03:30
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-02 00:52:55

import curses
import logging

class HUD(object):
    v_box_ht = 5
    v_box_wt = 30
    def __init__(self):
        self.display = curses.initscr()
        self.leftBox = self.display.subwin(self.v_box_ht, self.v_box_wt, 5, 5)
        self.rightBox = self.display.subwin(self.v_box_ht, self.v_box_wt, 5, 40)
        self.midBox = self.display.subwin(10, 60, 10, 10)
        self.touchBox = self.display.subwin(10, 60, 25, 10)
        self.configureHUD()
    def renderDisplay(self, state, speed, v1, v2, cap1, cap2, cap3, cap4, message):
        self.displayHeaderBar()
        self.displayInfo(v1, v2, state)
    def configureHUD(self):
        curses.noecho()
        self.display.nodelay(True)
        self.display.border(0)
        self.displayHeaderBar()
        # Create Left Window
        self.leftBox.box()
        # Create Right Window
        self.rightBox.box()
        self.leftBox.addstr(1, 5, "Voyager 1 Distance")
        self.rightBox.addstr(1, 5, "Voyager 2 Distance")
        # Create MidSetion Status
        self.midBox.box()
        self.midBox.addstr(1, 21, "Control Status")
        self.midBox.addstr(3, 5, "Current State: ")
        self.midBox.addstr(4, 5, "Current Speed: ")
        self.midBox.addstr(5, 5, "ProxV1 Status: ")
        self.midBox.addstr(6, 5, "ProxV2 Status: ")
        self.midBox.addstr(7, 5, "SlowDown Factor: 0x (in Green)")
        self.midBox.addstr(8, 5, "Timeout: 0 (in Green)")
        # Create Touch Box
        self.touchBox.box()
        self.touchBox.addstr(1, 21, "Action Traffic Log")
        self.displayRefresh()
        # Create Serial Box
    def displayHeaderBar(self):
        #Print the Greeting
        self.display.addstr(1, 14, 
            "**************   SentinelMC v3.2   **************")
        self.display.addstr(2, 14, 
            "**************  Updated June 2017  **************")
        self.displayRefresh()
    def displayRefresh(self):
        self.display.refresh()
        self.leftBox.refresh()
        self.rightBox.refresh()
        self.midBox.refresh()
        self.touchBox.refresh()
    def displayInfo(self, prox1, prox2, status):
        
        self.displayV1(prox1)
        self.displayV2(prox1)
        self.displayBar(prox1)
        self.displayRefresh()
    def displayBar (self, iteration):
        total = 30
        prefix = 'StartZone'
        suffix = 'RedZone'
        fill = '█'
        decimals = 1
        length = 35
        # Do work
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        if iteration > length:
            iteration = length
            suffix = 'MAX'
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        end = "%\r"
        buf = "%s |%s| %s %s %%\n" % (prefix, bar, suffix, percent)
        self.display.addstr(22, 5, buf)
        self.displayRefresh()
    def displayV1(self, distance):
        update = str(distance) +  " cm"
        self.display.addstr(8, 8, update)

        #if distance < 17.2:
        #    self.display.addstr(14, 30, "Within Green Zone", curses.A_UNDERLINE)
        #elif distance > 17.2 and distance < 30:
        #    self.display.addstr(14, 30, "Within Yellow Zone", curses.A_UNDERLINE)
        #    status = "Yellow"
        #else:
        #    self.display.addstr(14, 30, "RED ZONE, Beginning Timeout", curses.A_UNDERLINE)
        #    status = "Red"
        #return status
    def displayV2(self, distance):
        update = str(distance) +  " cm"
        screen.addstr(8, 43, update)

        #if distance < 17.2:
        #    self.display.addstr(14, 30, "Within Green Zone", curses.A_UNDERLINE)
        #elif distance > 17.2 and distance < 30:
        #    self.display.addstr(14, 30, "Within Yellow Zone", curses.A_UNDERLINE)
        #    status = "Yellow"
        #else:
        #    self.display.addstr(14, 30, "RED ZONE, Beginning Timeout", curses.A_UNDERLINE)
        #    status = "Red"
        #return status
    def displayState(self, state):
    def cleanup(self):
        curses.echo()
        curses.endwin()
    def msg(line):
        pass
        #logger.info(line)

