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

from gpiozero import Button
import time

btn0 = Button(5)
btn1 = Button(6)
btn2 = Button(13)
btn3 = Button(19)

pos = 0
def vainPositionRaw():
    ## Bit shifting button presses and OR'ing the result
    return int(btn3.is_pressed) << 3 | int(btn2.is_pressed) << 2 | \
        int(btn1.is_pressed) << 1 | int(btn0.is_pressed)
    

def vainDegrees():
    return vanPositionRaw * 22.5

