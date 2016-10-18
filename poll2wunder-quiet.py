#!/usr/bin/python

import os
import time
import threading
import logging
from gps import *
from wuSensors import bmp280
from wuSensors import sender

wuStation = "KCASANCA52"
wuPassword = "gzcdi8f0"
wuURI = "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php"
pollTime = 5 ## seconds
gpsd = None

class weatherPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while weatherp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer


## Init...
#logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
#                    level=logging.DEBUG)
logger = logging.getLogger("p2wu")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('p2wu.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

logger.debug("Starting up.")
weatherp = weatherPoller()
try:
    weatherp.start()
    while True:
        #It may take a second or two to get good data
        #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
        
        temperature,pressure,humidity = bmp280.readBME280All()
        if (gpsd.fix.mode == 3):
            req = sender.genReq(wuStation, wuPassword, gpsd.utc, (temperature * 1.8) + 32, pressure * 0.029529988)
            logger.debug("values:  %s" % req)
            logger.debug("Sending to WU: %s " % sender.sendReq(wuURI, req))
        else:
            logger.debug("Not sending yet.  GPS mode: %s", gpsd.fix.mode)
            
        time.sleep(pollTime) #set to whatever
        
except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    logger.debug("Killing Thread...")
    weatherp.running = False
    weatherp.join() # wait for the thread to finish what it's doing
logger.debug("Done.  Exiting.")
                  
