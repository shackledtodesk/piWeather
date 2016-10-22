#!/usr/bin/python

import os
import sys
import argparse
import time
import threading
import logging
import importlib
import json

from ConfigParser import SafeConfigParser

######## cmd line args
parser = argparse.ArgumentParser(description='RaspberryPi to WeatherUndergroun application.')
parser.add_argument('--config', default='pi2wu.cfg',
                    help='Configuration file to use. (default=pi2wu.cfg)')
parser.add_argument('--quiet', action='store_true',
                    help='Run quiet.  Do not display output.')
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

logger = logging.getLogger("pi2wu")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('pi2wu.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

## Sensors to Use Options
sensorPack = json.loads(cParser.get('sensors', 'sensors'))
snsrPack = {}
for snsr in sensorPack:
  logger.debug("loading sensor: %s" % snsr)
  if not args.quiet:
    print "loading sensor: %s" % snsr
  loadMe = "piSensors.%s" % snsr
  thing = importlib.import_module(loadMe)
  snsrPack[snsr] = thing.sensor()

pollTime = float(cParser.get('general', 'pollFrequency'))  ## seconds

def displayMeasurements(utcdate, data):
  print "clock: ", utcdate
  for mName, value in data.items():
    print mName, ": ", value

def pollSensors(sensors):
  results = {}

  for sensor, obj in sensors.items():
    ting = obj.getMeasurement()
    logger.debug("reading sensor: %s", sensor)
    if not args.quiet:
      print "reading sesor: ", ting
    results.update(ting)

  return results
    
###########################################
## Init...
#logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
#                    level=logging.DEBUG)

logger.debug("Starting up.")

from piWriters import wuSender
snd = wuSender.wuSender()

## Which method of getting UTC time do we use.
if cParser.get('general', 'timing') == "gpsd":
  from piWriters import gpsd
  cTime = gpsd.gpsdTime()
else:
  from piWriters import localTime
  cTime = localTime.localTime()
  
while True:
  snsrReturn = pollSensors(snsrPack)
  timeCheck = cTime.getTime()
  req = snd.genReq(wuStation, wuPassword, timeCheck, snsrReturn)
  logger.debug("values:  %s" % req)

  try:
    resp = snd.sendReq(wuURI, req)
    logger.debug("Sending to WU: %s" % resp)
    if not args.quiet:
      print "Sent to WU with response: %s" % resp
      displayMeasurements(timeCheck, snsrReturn)
  except:
    e = sys.exc_info()[0]
    logger.debug(e)

  print "poll time: %f" % pollTime
  time.sleep(pollTime)
        
logger.debug("Done.  Exiting.")
                  
