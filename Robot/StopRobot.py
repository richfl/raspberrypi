import sys
import RPi.GPIO as GPIO
from wheels import Wheels

GPIO.setmode(GPIO.BCM)

robot = Wheels()
robot.Stop()

GPIO.cleanup()