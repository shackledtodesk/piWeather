"""
Wind direction test.  I figured in 4 bits I can have 16 directional values
 0  - North
 1  - North North East
 2  - North East
 3  - East North East
 4  - East
  etc

Each bit == 22.5 degrees
Input GPIO pins used on Raspberry Pi 3:
   05 (pin 29, 2^0), 06 (pin 31, 2^1), 13 (pin 33, 2^2), 19 (pin 35, 2^3) 
"""

import json
from gpiozero import Button

class windDirection:

    btn0 = Button(5)
    btn1 = Button(6)
    btn2 = Button(13)
    btn3 = Button(19)

    def __init__(self):
        None
    
    def vainPositionRaw(self):
        ## global btn0, btn1, btn2, btn3
        ## Bit shifting button presses and OR'ing the result
        return int(self.btn3.is_pressed) << 3 | \
            int(self.btn2.is_pressed) << 2 | \
            int(self.btn1.is_pressed) << 1 | \
            int(self.btn0.is_pressed)
    

    def vainDegrees(self):
        return self.vainPositionRaw() * 22.5

    def getMeasurement(self):
        resp = "{ 'winddir': %s }" % self.vainDegrees()
        return json.dumps(resp)

if __name__ == '__main__':
    ## Little bit of testing of functionality
    sensor = windDirection()
    print "bit: ", sensor.vainPositionRaw()
    print "degrees: ", sensor.vainDegrees()
    print sensor.getMeasurement()
