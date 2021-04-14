import sys
import RPi.GPIO as GPIO

class wheel:
    def __init__(self, forwardpin, backwardpin, speed, frequency):
        self.wheelspeed = speed
        self.state = 's'

        GPIO.setup(forwardpin, GPIO.OUT)
        self.forwardpwm = GPIO.PWM(forwardpin, frequency)

        GPIO.setup(backwardpin, GPIO.OUT)
        self.backwardpwm = GPIO.PWM(backwardpin, frequency)

    def forward(self):
        if (self.state == 'b'):
            self.backwardpwm.stop()
        self.forwardpwm.start(self.wheelspeed)
        self.state = 'f'

    def reverse(self):
        if (self.state == 'f'):
            self.forwardpwm.stop()
        self.backwardpwm.start(self.wheelspeed)
        self.state = 'b'

    def stop(self):
        self.forwardpwm.stop()
        self.backwardpwm.stop()
        self.state = 's'

    def setspeed(self, speed):
        if (speed != self.wheelspeed):
            self.wheelspeed = speed
            if (self.state == 'f'):
                self.forward()
            elif (self.state == 'b'):
                self.reverse()

    def state(self):
        return self.state
