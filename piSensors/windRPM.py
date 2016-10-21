"""
Wind speed test.  Use a Hall Effect sensor to count. 

Pin used on Raspberry Pi 3:
    26 (pin 37)  
Count per Rotation == # of magnets
With 4 magnets means a count of 4 == 1 rotation
"""

from gpiozero import Button
import time, math, json

class windRPM:
    btn0 = Button(26)
    magnets = 4
    radius = 2.0 ## radius in centimeters
    rotations = 0
    elapsed = 0
    start_time = 0
    rpm = 0

    def __init__(self):
        self.start_time = time.time()
        self.btn0.when_pressed = self.rotationCount

    def rotationCount(self):
        if self.magnets == 0:
            self.magnets = 1

        self.rotations += 1
        self.elapsed = (time.time() - self.start_time) / self.magnets
        self.start_time = time.time()

        def calcRPM(self):
            if self.elapsed != 0:
                self.rpm = 1 / self.elapsed * 60
            return self.rpm

        def calcKPH(self):
            self.rpm = self.calcRPM()
            if self.elapsed != 0:
                circCM = (2 * math.pi) * self.radius
                distKM = circCM / 10000
                kph = distKM / self.elapsed * 3600
            else:
                kph = 0
            return kph

        def calcMPH(self):
            mph = calcKPH() * 0.621371
            return mph
    

        def getMeasurement(self):
            resp = "{ 'windspeedmph': %s }" % self.calcMPH

if __name__ == '__main__':
    ## Here just to test functionality
    wRPM = windRPM
    time.sleep(5)
    print "rpm: ", wRPM.calcRPM(), " pulses: ", wRPM.rotations, " mph: ", wRPM.calcMPH()
    
