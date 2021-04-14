import sys
import RPi.GPIO as GPIO

class wheel
    def __init__(self, forwardpin, backwardpin, speed, frequency):
        self.forwardpin = forwardpin
        self.backward.pin = backwardpin
        self.speed = speed
        self.state = 's'

        GPIO.setup(forwardpin, GPIO.OUT)
        self.forwardpwm = GPIO.PWM(forwardpin, frequency)

        GPIO.setup(backwardpin, GPIO.OUT)
        self.backwardpwm = GPIO.PWM(backwardpin, frequency)

    def forward(self):
        if (self.state == 'b'):
            backwardpwm.stop()
        forwardpwm.start(speed)
        self.state = 'f'

    def reverse(self):
        if (self.state == 'f'):
            forwardpwm.stop()
        backwardpwm.start(speed)
        self.state = 'b'

    def stop(self):
        forwardpwm.stop()
        backwardpwm.stop()
        self.state = 's'

    def setspeed(self, speed)
        if (speed != self.speed):
            self.speed = Speed
            if (self.state == 'f'):
                forward()
            elif (self.state == 'b'):
                reverse()

    def state(self):
        return self.state
