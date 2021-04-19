import sys
import RPi.GPIO as GPIO
from enum import Enum

class WheelDirection(Enum):
    Stop = 0
    Forward = 1
    Reverse = 2

class Wheel:
    def __init__(self, forwardpin, backwardpin, speed, frequency):
        self.wheelspeed = speed
        self.state = WheelDirection.Stop

        GPIO.setup(forwardpin, GPIO.OUT)
        self.forwardpwm = GPIO.PWM(forwardpin, frequency)

        GPIO.setup(backwardpin, GPIO.OUT)
        self.backwardpwm = GPIO.PWM(backwardpin, frequency)

    def Forward(self):
        if self.state == WheelDirection.Reverse:
            self.backwardpwm.stop()
        self.forwardpwm.start(self.wheelspeed)
        self.state = WheelDirection.Forward

    def Reverse(self):
        if self.state == WheelDirection.Forward:
            self.forwardpwm.stop()
        self.backwardpwm.start(self.wheelspeed)
        self.state = WheelDirection.Reverse

    def Stop(self):
        self.forwardpwm.stop()
        self.backwardpwm.stop()
        self.state = WheelDirection.Stop

    def SetSpeed(self, speed):
        if speed != self.wheelspeed:
            self.wheelspeed = speed
            if self.state == WheelDirection.Forward:
                self.forward()
            elif self.state == WheelDirection.Reverse:
                self.reverse()

    def State(self):
        return self.state
