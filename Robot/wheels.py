import sys
import RPi.GPIO as GPIO
from wheel import wheel

class wheels:
    def __init__(self, speed = 80, frequency = 1000):
        self.Direction = 's'
        self.robotspeed = speed
        self.Frequency = frequency

        GPIO.setmode(GPIO.BOARD)

        self.wheels = {}
        self.wheels['fl'] = wheel(16, 15, self.robotspeed, self.Frequency)
        self.wheels['fr'] = wheel(22, 18, self.robotspeed, self.Frequency)
        self.wheels['bl'] = wheel(13, 10, self.robotspeed, self.Frequency)
        self.wheels['br'] = wheel(8, 33, self.robotspeed, self.Frequency)
        self.stop()

    def stop(self):
        self.wheels['fl'].stop()
        self.wheels['fr'].stop()
        self.wheels['bl'].stop()
        self.wheels['br'].stop()

    def Forward(self):
        if (self.Direction != 'f'):
            self.stop()
            self.Direction = 'f'
            self.wheels['fl'].forward()
            self.wheels['fr'].forward()
            self.wheels['br'].forward()
            self.wheels['bl'].forward()

    def Backward(self):
        if (self.Direction != 'b'):
            self.stop()
            self.Direction = 'b'
            self.wheels['fl'].reverse()
            self.wheels['fr'].reverse()
            self.wheels['br'].reverse()
            self.wheels['bl'].reverse()
                                                                
    def SpinRight(self):
        if (self.Direction != 'r'):
            self.stop()
            self.Direction = 'r'
            self.wheels['fl'].forward()
            self.wheels['fr'].reverse()
            self.wheels['br'].reverse()
            self.wheels['bl'].forward()

    def SpinLeft(self):
        if (self.Direction != 'l'):
            self.stop()
            self.Direction = 'l'
            self.wheels['fl'].reverse()
            self.wheels['fr'].forward()
            self.wheels['br'].forward()
            self.wheels['bl'].reverse()

    def MoveRight(self):
        if (self.Direction != 'mr'):
            self.stop()
            self.Direction = 'mr'
            self.wheels['fl'].forward()
            self.wheels['fr'].reverse()
            self.wheels['br'].forward()
            self.wheels['bl'].reverse()

    def MoveLeft(self):
        if (self.Direction != 'ml'):
            self.stop()
            self.Direction = 'ml'
            self.wheels['fl'].reverse()
            self.wheels['fr'].forward()
            self.wheels['br'].reverse()
            self.wheels['bl'].forward()

    def Speed(self, newspeed):
        if (self.robotspeed != newspeed):
            self.robotspeed = newspeed
            self.wheels['fl'].setspeed(newspeed)
            self.wheels['fr'].setspeed(newspeed)
            self.wheels['bl'].setspeed(newspeed)
            self.wheels['br'].setspeed(newspeed)

