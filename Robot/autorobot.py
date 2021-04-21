import sys
import RPi.GPIO as GPIO
from wheels import Wheels
from ultrasonic import DistanceSensors

sensors = DistanceSensors()
robot = Wheels()

try:
    # Determine space around robot and find biggest open space
    if not(sensors.StartScanner(0.5, True)):
        raise "Distance sensors not working"

    # work out how long to spin to rotate 45 degrees - remember speed

    # do minimal rotate so either front or back is pointing to biggest space

    while true:
        # move forward\back based on biggest space
        # speed will depend on available distance

        # decelerate as approach barrier
        # do minimal spin right\left to new biggest space and determine optimal direction

finally:
    sensors.StopScanner()
    robot.Stop()
    GPIO.cleanup()