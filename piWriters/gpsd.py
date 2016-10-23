from gps import *
from time import sleep
import threading

class gpsdTime(threading.Thread):
  
  def __init__(self):
    threading.Thread.__init__(self)
    self.gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.gpsd.next()
    self.gpsd.running = True
    while self.gpsd.fix.mode != 3:
      self.gpsd.next()

  def run(self):
    while self.gpsd.running:
      self.gpsd.next()

  def stop(self):
    self.gpsd.running = False
    self.join()
      
  def getTime(self):
    self.gpsd.next()
    return self.gpsd.utc

if __name__ == '__main__':
  something = gpsdTime()
  print something.getTime()
  ## print something.getTime
