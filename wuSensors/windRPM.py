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

def calcRPM():
    global rotations, start_time, elapsed, rpm
    if elapsed != 0:
        rpm = 1 / elapsed * 60
    return rpm

def calcKPH():
    rpm = calcRPM()
    circCM = (2 * math.pi) * radius
    distKM = circCM / 10000
    return distKM / elasped * 3600

def calcMPH():
    return calcKPH() * 0.621371    

def initButton():
    global start_time
    start_time = time.time()
    btn0.when_pressed = rotationCount

if __name__ == '__main__':
    initButton()
    sleep = 5
    while True:
        time.sleep(sleep)
        print "rpm: ", calcRPM(), " pulses: ", rotations, " mph: ", calcMPH()
    
