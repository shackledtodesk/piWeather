from gps import *
from time import sleep
import threading
import traceback

class gpsdTime(threading.Thread):
  
  def __init__(self):
    threading.Thread.__init__(self)
    try:
      self.gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    except:
      traceback.print_exc()

    self.gpsd.running = True
    self.gpsd.next()
    ## Don't return from init until a Fix is made
    while self.gpsd.fix.mode != 3:
      self.gpsd.next()

  def run(self):
    while self.gpsd.running:
      self.gpsd.next()

  def stop(self):
    self.gpsd.running = False
    self.join()
      
  def getTime(self):
    ##self.gpsd.next()
    return self.gpsd.utc

if __name__ == '__main__':
  something = gpsdTime()
  print something.getTime()
  ## print something.getTime
