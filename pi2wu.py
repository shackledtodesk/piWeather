#!/usr/bin/python

import os
import sys
import signal
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

logger = logging.getLogger("pi2wu")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('pi2wu.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

pollTime = float(cParser.get('general', 'pollFrequency'))  ## seconds

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

from piWriters import wuSender
snd = wuSender.wuSender(cParser)

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


def signal_handler(signum, frame):
  logger.debug("Caught signal: %s", signum)
  print "caught signal:", signum
  sys.exit(0)
signal.signal(signal.SIGTERM,signal_handler)
signal.signal(signal.SIGINT,signal_handler)

###########################################
## Init...
logger.debug("Starting up.")

## Which method of getting UTC time do we use.
if cParser.get('general', 'timing') == "gpsd":
  logger.debug("Loading gps timing module")
  from piWriters import gpsd
  cTime = gpsd.gpsdTime()
  cTime.start()  
else:
  logger.debug("Using local machine clock for UTC.")
  from piWriters import localTime
  cTime = localTime.localTime()
  
while True:
  try:
    snsrReturn = pollSensors(snsrPack)
    timeCheck = cTime.getTime()
    req = snd.genReq(timeCheck, snsrReturn)
    logger.debug("values:  %s" % req)
    
    try:
      resp = snd.sendReq(req)
      logger.debug("Sending to WU: %s" % resp)
      if not args.quiet:
        print "Sent to WU with response: %s" % resp
        displayMeasurements(timeCheck, snsrReturn)
    except Exception:
      e = sys.exc_info()[0]
      logger.debug(e)

    if not args.quiet:
      print "Waiting..."
    time.sleep(pollTime)
      
  except (KeyboardInterrupt, SystemExit):
    cTime.stop()
    logger.debug("Done.  Exiting.")
    break
