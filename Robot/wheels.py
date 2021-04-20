import sys
import RPi.GPIO as GPIO
from enum import Enum
from wheel import Wheel

class Axle(Enum):
    FrontLeft = 1
    FrontRight = 2
    BackLeft = 3
    BackRight = 4

class Direction(Enum):
    Stop = 0
    Forward = 1
    Reverse = 2
    SpinRight = 3
    SpinLeft = 4
    MoveRight = 5
    MoveLeft = 6
    ForwardRight = 7
    ForwardLeft = 8
    ReverseRight = 9
    ReverseLeft = 10

class Wheels:
    def __init__(self, speed = 80, frequency = 1000):
        self.direction = Direction.Stop
        self.robotspeed = speed

        GPIO.setmode(GPIO.BCM)

        self.wheels = {}
        self.wheels[Axle.FrontLeft] = Wheel(23, 22, self.robotspeed, frequency)
        self.wheels[Axle.FrontRight] = Wheel(25, 24, self.robotspeed, frequency)
        self.wheels[Axle.BackLeft] = Wheel(27, 15, self.robotspeed, frequency)
        self.wheels[Axle.BackRight] = Wheel(14, 13, self.robotspeed, frequency)
        self.Stop()

    def Stop(self):
        self.direction = Direction.Stop
        self.wheels[Axle.FrontLeft].Stop()
        self.wheels[Axle.FrontRight].Stop()
        self.wheels[Axle.BackLeft].Stop()
        self.wheels[Axle.BackRight].Stop()

    def Forward(self):
        if self.direction != Direction.Forward:
            self.Stop()
            self.direction = Direction.Forward
            self.wheels[Axle.FrontLeft].Forward()
            self.wheels[Axle.FrontRight].Forward()
            self.wheels[Axle.BackRight].Forward()
            self.wheels[Axle.BackLeft].Forward()

    def Backward(self):
        if self.direction != Direction.Reverse:
            self.Stop()
            self.direction = Direction.Reverse
            self.wheels[Axle.FrontLeft].Reverse()
            self.wheels[Axle.FrontRight].Reverse()
            self.wheels[Axle.BackRight].Reverse()
            self.wheels[Axle.BackLeft].Reverse()
                                                                
    def SpinRight(self):
        if (self.direction != Direction.SpinRight):
            self.Stop()
            self.direction = Direction.SpinRight
            self.wheels[Axle.FrontLeft].Forward()
            self.wheels[Axle.FrontRight].Reverse()
            self.wheels[Axle.BackRight].Reverse()
            self.wheels[Axle.BackLeft].Forward()

    def SpinLeft(self):
        if self.direction != Direction.SpinLeft:
            self.Stop()
            self.direction = Direction.SpinLeft
            self.wheels[Axle.FrontLeft].Reverse()
            self.wheels[Axle.FrontRight].Forward()
            self.wheels[Axle.BackRight].Forward()
            self.wheels[Axle.BackLeft].Reverse()

    def MoveRight(self):
        if self.direction != Direction.MoveRight:
            self.Stop()
            self.direction = Direction.MoveRight
            self.wheels[Axle.FrontLeft].Forward()
            self.wheels[Axle.FrontRight].Reverse()
            self.wheels[Axle.BackRight].Forward()
            self.wheels[Axle.BackLeft].Reverse()

    def MoveLeft(self):
        if self.direction != Direction.MoveLeft:
            self.Stop()
            self.direction = Direction.MoveLeft
            self.wheels[Axle.FrontLeft].Reverse()
            self.wheels[Axle.FrontRight].Forward()
            self.wheels[Axle.BackRight].Reverse()
            self.wheels[Axle.BackLeft].Forward()

    def MoveForwardRight(self):
        if self.direction != Direction.ForwardRight:
            self.Stop()
            self.direction = Direction.ForwardRight
            self.wheels[Axle.FrontLeft].Forward()
            self.wheels[Axle.FrontRight].Stop()
            self.wheels[Axle.BackRight].Forward()
            self.wheels[Axle.BackLeft].Stop()

    def MoveForwardLeft(self):
        if self.direction != Direction.ForwardLeft:
            self.Stop()
            self.direction = Direction.ForwardLeft
            self.wheels[Axle.FrontRight].Forward()
            self.wheels[Axle.FrontLeft].Stop()
            self.wheels[Axle.BackLeft].Forward()
            self.wheels[Axle.BackRight].Stop()

    def MoveBackwardLeft(self):
        if self.direction != Direction.ReverseLeft:
            self.Stop()
            self.direction = Direction.ReverseLeft
            self.wheels[Axle.FrontLeft].Reverse()
            self.wheels[Axle.FrontRight].Stop()
            self.wheels[Axle.BackRight].Reverse()
            self.wheels[Axle.BackLeft].Stop()

    def MoveBackwardRight(self):
        if self.direction != Direction.ReverseRight:
            self.Stop()
            self.direction = Direction.ReverseRight
            self.wheels[Axle.FrontRight].Reverse()
            self.wheels[Axle.FrontLeft].Stop()
            self.wheels[Axle.BackLeft].Reverse()
            self.wheels[Axle.BackRight].Stop()

    def Speed(self, newspeed):
        if self.robotspeed != newspeed:
            self.robotspeed = newspeed
            self.wheels[Axle.FrontLeft].SetSpeed(newspeed)
            self.wheels[Axle.FrontRight].SetSpeed(newspeed)
            self.wheels[Axle.BackLeft].SetSpeed(newspeed)
            self.wheels[Axle.BackRight].SetSpeed(newspeed)

