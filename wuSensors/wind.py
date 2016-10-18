"""
Wind direction test.  I figured in 4 bits I can have 16 directional values
 0  - North
 1  - North North East
 2  - North East
 3  - East North East
 4  - East
  etc
"""

from gpiozero import LED,RGBLED,Button
import time

btn0 = Button(20)
btn1 = Button(21)

pos = 0
while True:
    ## Bit shifting button presses and OR'ing the result
    pos = int(btn1.is_pressed) << 1 | int(btn0.is_pressed)
    print pos
    pos = 0
    time.sleep(10)
    
