#!/usr/bin/python

import os
import sys
import argparse
import time
import threading
import logging
from ConfigParser import SafeConfigParser
from gps import *

from piSensors import bmp280
from piWriters import wuSender

######## cmd line args
parser = argparse.ArgumentParser(description='RaspberryPi to WeatherUndergroun application.')
parser.add_argument('--config', default='pi2wu.cfg', help='Configuration file to use. (default=pi2wu.cfg)')
parser.add_argument('--quiet', action='store_true', help='Run quiet.  Do not display output.')
args = parser.parse_args()

######## get config
cParser = SafeConfigParser()
cParser.read(args.config)

## WeatherUnderground Options
wuStation = cParser.get('wunderground','station')
wuPassword = cParser.get('wunderground','password')

if cParser.has_option('wunderground','uri'):
  wuURI = cParser.get('wunderground','uri')
else:
  wuURI = "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php"


## Sensors to Use Options
sensorPack = json.loads(cParser.get('sensors', 'sensors'))

pollTime = 10 ## seconds
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
      gpsd.next() 


def displayMeasurements(utcdate, data):
  print "clock: ", utcdate
  for mName, value in data.items():
    print mName, ": ", value
  
## Init...
#logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
#                    level=logging.DEBUG)
logger = logging.getLogger("pi2wu")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('pi2wu.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

logger.debug("Starting up.")
weatherp = weatherPoller()
tph = bmp280.bmp280()
try:
    weatherp.start()
    while True:
        #It may take a second or two to get good data
        #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
        
        temperature,pressure,humidity = tph.readBME280All()
        if (gpsd.fix.mode == 3):
          req = sender.genReq(wuStation, wuPassword, gpsd.utc, (temperature * 1.8) + 32, pressure * 0.029529988)
          logger.debug("values:  %s" % req)

          if not args.quiet:
            displayMeasurements(gpsd.utc, { "temp": temperature, "pressure": pressure })
          
          try:
            logger.debug("Sending to WU: %s " % sender.sendReq(wuURI, req))
          except:
            e = sys.exc_info()[0]
            logger.debug(e)
        else:
          logger.debug("Not sending yet.  GPS mode: %s", gpsd.fix.mode)
            
        time.sleep(pollTime) #set to whatever
        
except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    logger.debug("Killing Thread...")
    weatherp.running = False
    weatherp.join() # wait for the thread to finish what it's doing
logger.debug("Done.  Exiting.")
                  
