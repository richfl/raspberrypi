import sys
import RPi.GPIO as GPIO
from wheels import Wheels

robot = Wheels()
x = 's'

try:
    while x != 'e':
        x=input()

        if x =='f':
            robot.Forward()
        elif x == 'b':
            robot.Backward()
        elif x == 's' or x == '0':
            robot.Stop()
        elif x == 'l':
            robot.SpinLeft()
        elif x == 'r':
            robot.SpinRight()
        elif x == 'mr':
            robot.MoveRight()
        elif x == 'ml':
            robot.MoveLeft()
        elif x == 'fr':
            robot.MoveForwardRight()
        elif x == 'fl':
            robot.MoveForwardLeft()
        elif x == 'br':
            robot.MoveBackwardRight()
        elif x == 'bl':
            robot.MoveBackwardLeft()
        elif x >= '4' and x <= '9':
            robot.Speed(int(x) * 10)
        elif x > '0' and x <= '3':
            robot.Speed(100)
finally:
    GPIO.cleanup()