#!/usr/bin/python

import os
import time
import threading
from gps import *
from wuSensors import bmp280
from wuSensors import sender

wuStation = "KCASANCA52"
wuPassword = "gzcdi8f0"
wuURI = "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php"
pollTime = 20 ## seconds
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
weatherp = weatherPoller()
try:
    weatherp.start()
    while True:
        #It may take a second or two to get good data
        #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
        
        os.system('clear')
        temperature,pressure,humidity = bmp280.readBME280All()
        print
        print ' GPS reading'
        print '----------------------------------------'
        print 'temperature ' , (temperature * 1.8) + 32, "F"
        print 'pressure    ' , pressure, "hPa"
        print 'latitude    ' , gpsd.fix.latitude
        print 'longitude   ' , gpsd.fix.longitude
        print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
        print 'altitude (m)' , gpsd.fix.altitude
        print 'eps         ' , gpsd.fix.eps
        print 'epx         ' , gpsd.fix.epx
        print 'epv         ' , gpsd.fix.epv
        print 'ept         ' , gpsd.fix.ept
        print 'speed (m/s) ' , gpsd.fix.speed
        print 'climb       ' , gpsd.fix.climb
        print 'track       ' , gpsd.fix.track
        print 'mode        ' , gpsd.fix.mode
        print
        print 'sats        ' , gpsd.satellites

        print
        if (gpsd.fix.mode == 3):
            req = sender.genReq(wuStation, wuPassword, gpsd.utc, (temperature * 1.8) + 32, pressure * 0.029529988)
            print "Values: %s" % req
            print "Sending to WU: %s " % sender.sendReq(wuURI, req)
        time.sleep(pollTime) #set to whatever
        
except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    weatherp.running = False
    weatherp.join() # wait for the thread to finish what it's doing
print "Done.\nExiting."
                  
