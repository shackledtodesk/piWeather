"""
Wind speed test.  Use a Hall Effect sensor to count. 

Pin used on Raspberry Pi 3:
    26 (pin 37)  
Count per Rotation == # of magnets
With 4 magnets means a count of 4 == 1 rotation
"""

from gpiozero import Button
import time, math

btn0 = Button(26)
magnets = 4
radius = 2.0 ## radius in centimeters
rotations = 0
elapsed = 0
start_time = 0
rpm = 0

def rotationCount():
    global rotations, start_time, elapsed, magnets

    if magnets == 0:
        magnets = 1

    rotations += 1
    elapsed = (time.time() - start_time) / magnets
    start_time = time.time()

def calcRPM(dTime = 0):
    global rotations, start_time, rpm
    if dTime != 0:
        rpm = 1 / dTime * 60
    return rpm

def calcKPH(dTime = 0):
    global radius
    rpm = calcRPM()
    if dTime != 0:
        circCM = (2 * math.pi) * radius
        distKM = circCM / 10000
        kph = distKM / dTime * 3600
    else:
        kph = 0
    return kph

def calcMPH(dTime = 0):
    mph = calcKPH(dTime) * 0.621371
    return mph
    

def initButton():
    global start_time
    start_time = time.time()
    btn0.when_pressed = rotationCount

if __name__ == '__main__':
    ## Here just to test functionality
    initButton()
    time.sleep(5)
    print "rpm: ", calcRPM(elapsed), " pulses: ", rotations, " mph: ", calcMPH(elapsed)
    
