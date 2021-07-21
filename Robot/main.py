import sys
import time
import RPi.GPIO as GPIO
from autorobot import AutoRobot

GPIO.setmode(GPIO.BCM)
autonomousRobot = AutoRobot(0.1)
time.sleep(1) # allow sensors time to complete a scan

try:
    # work out if we want to go forwards or backwards based on available space
    currentDirection = autonomousRobot.GetFurthestEnd()
    
    # if we have less than 10 cm left in our preferred direction see if another direction would be better
    if currentDirection[1] < 20.0:
        currentDirection = autonomousRobot.RotateToBiggestSpace()

    autonomousRobot.SetSpeedBasedOnDistance(currentDirection[1])
    autonomousRobot.robot.Move(currentDirection[0])
    loop = 1

    while True:
        currentDirection = autonomousRobot.GetDistanceToNextObstacle()
        nearestObstacle = autonomousRobot.GetNearestObstacleInDirectionOfTravel(currentDirection[0])

        # display current metrics every 4th loop
        loop -= 1
        if loop == 0:
            loop = 4
            print(currentDirection, nearestObstacle)

        # adjust speed as we move relative to any obstacles in front of us, factor in any obstacles to the side
        # take the average distance between nearest front obstacle and side obstacle if the nearest obstacle isn't directly infront of us
        speedDistance = min(currentDirection[1], (nearestObstacle + currentDirection[1]) / 2)
        autonomousRobot.SetSpeedBasedOnDistance(speedDistance)

        # change direction if:
        # there is less than 25cm left in direction of travel  
        # or there is an obstacle anywhere infront of us < 10cm
        # or we haven't made forward progress since the last scan
        if currentDirection[1] < 25.0 or nearestObstacle < 10.0 or autonomousRobot.AreWeStuck(currentDirection[0], currentDirection[1]): 
            currentDirection = autonomousRobot.RotateToBiggestSpace()
            autonomousRobot.SetSpeedBasedOnDistance(currentDirection[1])
            autonomousRobot.robot.Move(currentDirection[0])

        autonomousRobot.UpdatePosition(currentDirection[0], currentDirection[1])
        time.sleep(0.5)

finally:
    autonomousRobot.robot.Stop()
    autonomousRobot.sensors.StopScanner()
    GPIO.cleanup()