import sys
import time
import RPi.GPIO as GPIO
from wheels import Wheels, Direction
from ultrasonic import DistanceSensors
from servos import ServoDirection, ServoEnd

class AutoRobot:
    def __init__(self)
        self.sensors = DistanceSensors()
        self.robot = Wheels()
        
        # start distance scanning
        if not(sensors.StartScanner(0.5, True)):
            raise "Distance sensors not working"

    def GetDistanceToNextObstacle(self):
    '''
        Returns the remaining distance in CMs in the current direction of travel
        Returns space in forward direction if stopped or rotating 
    '''
        distance = -1.0
        if self.robot.direction == Direction.Forward or self.robot.direction == Direction.Stop or \
            self.robot.direction == Direction.SpinLeft or self.robot.direction == Direction.SpinRight:
            distance = self.sensors.frontDistance[ServoDirection.Ahead]
        elif self.robot.direction == Direction.Reverse:
            distance = self.sensors.backDistance[ServoDirection.Ahead]
        elif self.robot.direction == Direction.ForwardRight:
            distance = self.sensors.frontDistance[ServoDirection.OffRight]
        elif self.robot.direction == Direction.ForwardLeft:
            distance = self.sensors.frontDistance[ServoDirection.OffLeft]
        elif self.robot.direction == Direction.ReverseLeft:
            distance = self.sensors.backDistance[ServoDirection.OffLeft]
        elif self.robot.direction == Direction.ReverseRight:
            distance = self.sensors.backDistance[ServoDirection.OffRight]
        elif self.robot.direction == Direction.MoveRight:
            distance = self.sensors.frontDistance[ServoDirection.Right]
        elif self.robot.direction == Direction.MoveLeft:
            distance = self.sensors.frontDistance[ServoDirection.Left]
        return distance

    def GetFurthestEnd(self):
    '''
        Work out if there is more space infront or behind and ignore sides
    '''
        if sensors.backDistance[ServoDirection.Ahead] > sensors.frontDistance[ServoDirection.Ahead]:
            return (Direction.Reverse, sensors.backDistance[ServoDirection.Ahead])
        else:
            return (Direction.Forward, sensors.frontDistance[ServoDirection.Ahead])

    def GetMaxDistanceDirection(self):
    '''
        Returns the sensor direction with the most space and what that distance is
    '''
        maxRearDistance = max(self.sensors.backDistance.values())
        maxFrontDistance = max(self.sensors.frontDistance.values())

        if maxRearDistance > maxFrontDistance:
            res = [key for key in sensors.backDistance if self.sensors.backDistance[key] >= maxRearDistance]
            return (ServoEnd.Back, res[0], maxRearDistance)
        else:
            res = [key for key in sensors.frontDistance if self.sensors.frontDistance[key] >= maxFrontDistance]
            return (ServoEnd.Front, res[0], maxFrontDistance)

    def GetMinDistanceDirection(self):
    '''
    Returns the sensor direction with the least space and what that distance is
    '''
        minRearDistance = min(self.sensors.backDistance.values())
        minFrontDistance = min(self.sensors.frontDistance.values())

        if minRearDistance < minFrontDistance:
            res = [key for key in self.sensors.backDistance if self.sensors.backDistance[key] == minRearDistance]
            return (ServoEnd.Back, res[0], minRearDistance)
        else:
            res = [key for key in self.sensors.frontDistance if self.sensors.frontDistance[key] == minFrontDistance]
            return (ServoEnd.Front, res[0], minFrontDistance)

    def SetSpeedBasedOnDistance(self, distance):
        if distance < 5.0:
            self.robot.Stop()
        elif distance < 10.0:
            self.robot.Speed(60)
        elif distance < 20.0:
            self.robot.Speed(70)
        elif distance < 30.0:
            self.robot.Speed(80) 
        else:
            self.robot.Speed(90) 
        return self.robot.robotspeed

    def RotateToBiggestSpace(self):
    ''' 
        rotates so either front or rear is pointing to biggests space.
        returns whether forwards or reverse is best and how much space there is in that direction
    '''
        while True: # repeat until the front or back is pointing to the biggest space
            preferredDirection = self.GetMaxDistanceDirection()
    
            # if the best direction is forward or reverse don't spin and return
            if preferredDirection[1] == ServoDirection.Ahead:
                if preferredDirection[0] == ServoEnd.Front:
                    return Direction.Forward, preferredDirection[2]
                else:
                    return Direction.Reverse, preferredDirection[2]

            self.robot.Speed(80)
            
            # work out whether to spin right or left
            if (preferredDirection[0] == ServoEnd.Front and 
                (preferredDirection[1] == ServoDirection.OffRight or preferredDirection[1] == ServoDirection.Right)) or \
                (preferredDirection[0] == ServoEnd.Back and 
                (preferredDirection[1] == ServoDirection.OffLeft or preferredDirection[1] == ServoDirection.Left)):
                self.robot.SpinRight()
            else:
                self.robot.SpinLeft()

            if ServoDirection.OffLeft or ServoDirection.OffRight:
                time.sleep(0.5) # rotate 45 degrees
            else: 
                time.sleep(1) # rotate 90 degrees
            self.robot.Stop()

            # wait to get new set of distance readings - worst case is potentially 4 seconds
            time.sleep(3)

try:
    GPIO.setmode(GPIO.BCM)
    autonomousRobot = AutoRobot()

    # work out if we want to go forwards or backwards based on available space
    currentDirection = autonomousRobot.GetFurthestEnd()
    
    # if we have less than 10 cm left in our preferred direction see if another direction would be better
    while currentDirection[1] < 10.0:
        autonomousRobot.RotateToBiggestSpace()
        currentDirection = autonomousRobot.GetFurthestEnd()
    autonomousRobot.SetSpeedBasedOnDistance(currentDirection[1])
    autonomousRobot.robot.Move(currentDirection[0])
  
    while True:
        # adjust speed as we get closer to a barrier
        autonomousRobot.SetSpeedBasedOnDistance(GetDistanceToNextObstacle())

        # change direction if there is less than 10cm left in direction of travel  
        if autonomousRobot.GetDistanceToNextObstacle() < 10.0: 
            newDirection = autonomousRobot.RotateToBiggestSpace()
            autonomousRobot.robot.Move(newDirection[0])

finally:
    autonomousRobot.robot.Stop()
    autonomousRobot.sensors.StopScanner()
    GPIO.cleanup()