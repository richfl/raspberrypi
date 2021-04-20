import sys
import time
from adafruit_servokit import ServoKit
from enum import IntEnum

class ServoEnd(IntEnum):
    Front = 1
    Back = 2

class ServoDirection(IntEnum):
    Right = 0
    OffRight = 45
    Ahead = 90
    OffLeft = 135
    Left = 180

class Servos:
    def __init__(self, frontPort, backPort):
        self.front = frontPort
        self.back = backPort
        self.kit = ServoKit(channels=16)
        self.scanArray = [ServoDirection.Right, ServoDirection.OffRight, ServoDirection.Ahead, ServoDirection.OffLeft, ServoDirection.Left]
        self.scanIndex = 0
        self.scanDirection = 1

    def MoveServo(self, end, direction):
        if end == ServoEnd.Front:
            self.kit.servo[self.front].angle = direction
        else:
            self.kit.servo[self.back].angle = 180 - direction

    def NextScanPosition(self):
        if (self.scanDirection == 1 and self.scanIndex == (len(self.scanArray) - 1)) or (self.scanDirection == -1 and self.scanIndex == 0):
            self.scanDirection = -self.scanDirection
        self.MoveServo(ServoEnd.Front, self.scanArray[self.scanIndex])
        self.MoveServo(ServoEnd.Back, self.scanArray[self.scanIndex])
        self.scanIndex += self.scanDirection
        time.sleep(0.1)
        return self.scanArray[self.scanIndex]

    def FirstScanPosition(self):
        self.scanIndex = 0
        self.scanDirection = 1
        self.MoveServo(ServoEnd.Front, ServoDirection.Right)
        self.MoveServo(ServoEnd.Back, ServoDirection.Right)
        time.sleep(0.5)
        return self.scanArray[self.scanIndex]

#servos = Servos(6, 7)
#servos.FirstScanPosition()
#while True:
#    position = servos.NextScanPosition()
#    print(position)