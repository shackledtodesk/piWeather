"""
Wind speed test.  Use a Hall Effect sensor to count. 
"""

from gpiozero import LED,RGBLED,Button
import time

btn0 = Button(20) 
btn1 = Button(21)

def rotationCount():
    global rotations
    rotations += 1
    

rotations = 0
btn0.when_pressed = rotationCount
sleep = 5
while True:
    time.sleep(sleep)
    rpm = rotations * (60 / sleep)
    print rpm, "rpm ", rotations
    rotations = 0
    
