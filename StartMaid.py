# -*- coding: utf-8 -*-
# @Author: Eddie Ruano
# @Date:   2017-06-16 12:57:01
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-16 13:43:23
import os, os.path
import logging
import sys
import time
from pathlib import Path

def main():

    LogLevel = logging.DEBUG        ## Change this later
    LogLocation = "Logs/MaidLog.txt"
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
    Houston.info("Maid Logger has been created.")

    runLock = Path("ON.dat")
    if runLock.is_file():
        Houston.info("ON.dat was found. Removing and resetting JSONs.")
        os.remove("ON.dat")
    time.sleep(3)
    sys.exit(0)

if __name__ == "__main__":
    # Create Controller Loop
    main()