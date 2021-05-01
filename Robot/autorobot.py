import sys
import time
import RPi.GPIO as GPIO
from wheels import Wheels, Direction
from ultrasonic import DistanceSensors
from servos import ServoDirection, ServoEnd

class AutoRobot:
    def __init__(self):
        self.sensors = DistanceSensors()
        self.robot = Wheels()

        self.previousDistance = -1.0
        self.previousDirection = Direction.Stop
        
        # start distance scanning
        if not(self.sensors.StartScanner(0.1, True)):
            raise "Distance sensors not working"

    def GetDistanceToNextObstacle(self):
        '''
            Returns the remaining direction, distance in CMs in the current direction of travel
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
        return self.robot.direction, distance

    def GetFurthestEnd(self):
        '''
            returns direction, distance
            Work out if there is more space infront or behind and ignore sides
        '''
        if self.sensors.backDistance[ServoDirection.Ahead] > self.sensors.frontDistance[ServoDirection.Ahead]:
            print("Furthest = Reverse", self.sensors.backDistance[ServoDirection.Ahead])
            return (Direction.Reverse, self.sensors.backDistance[ServoDirection.Ahead])
        else:
            print("Furthest = Forward", self.sensors.frontDistance[ServoDirection.Ahead])
            return (Direction.Forward, self.sensors.frontDistance[ServoDirection.Ahead])

    def GetMaxDistanceDirection(self):
        '''
            returns servo end, servo direction, distance
            Returns the sensor direction with the most space and what that distance is
        '''
        maxRearDistance = max(self.sensors.backDistance.values())
        maxFrontDistance = max(self.sensors.frontDistance.values())

        if maxRearDistance > maxFrontDistance:
            res = [key for key in self.sensors.backDistance if self.sensors.backDistance[key] >= maxRearDistance]
            return (ServoEnd.Back, res[0], maxRearDistance)
        else:
            res = [key for key in self.sensors.frontDistance if self.sensors.frontDistance[key] >= maxFrontDistance]
            return (ServoEnd.Front, res[0], maxFrontDistance)

    def GetMinDistanceDirection(self):
        '''
            returns servo end, servo direction, distance
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
        if distance < 20.0:
            self.robot.Stop()
        elif distance < 40.0:
            self.robot.Speed(40)
        elif distance < 60.0:
            self.robot.Speed(50)
        elif distance < 100.0:
            self.robot.Speed(80) 
        else:
            self.robot.Speed(100) 
        return self.robot.robotspeed

    def RotateToBiggestSpace(self):
        ''' 
            returns direction, distance in new direction of travel
            Rotates so either front or rear is pointing to biggests space.
        '''
        while True: # repeat until the front or back is pointing to the biggest space
            preferredDirection = self.GetMaxDistanceDirection()
            print("rotating, preferred direction is ", preferredDirection)
            # if the best direction is forward or reverse don't spin and return
            if preferredDirection[1] == ServoDirection.Ahead or \
                preferredDirection[1] == ServoDirection.OffLeft or \
                preferredDirection[1] == ServoDirection.OffRight:
                if preferredDirection[0] == ServoEnd.Front:
                    return Direction.Forward, preferredDirection[2]
                else:
                    return Direction.Reverse, preferredDirection[2]

            self.robot.Speed(70)
            
            # work out whether to spin right or left
            if (preferredDirection[0] == ServoEnd.Front and 
                (preferredDirection[1] == ServoDirection.OffRight or preferredDirection[1] == ServoDirection.Right)) or \
                (preferredDirection[0] == ServoEnd.Back and 
                (preferredDirection[1] == ServoDirection.OffLeft or preferredDirection[1] == ServoDirection.Left)):
                self.robot.SpinRight()
            else:
                self.robot.SpinLeft()

            if ServoDirection.OffLeft or ServoDirection.OffRight:
                time.sleep(0.3) # rotate 45 degrees
            else: 
                time.sleep(0.6) # rotate 90 degrees
            self.robot.Stop()

            # wait to get new set of distance readings
            time.sleep(1)

    def AreWeStuck(self, direction, distance):
        if abs(distance - self.previousDistance) < 1.0 and direction == self.previousDirection:
            print("Stuck")
            return True
        return False

    def UpdatePosition(self, direction, distance):
        self.previousDirection = direction
        self.previousDistance = distance

GPIO.setmode(GPIO.BCM)
autonomousRobot = AutoRobot()
time.sleep(1)

try:
    # work out if we want to go forwards or backwards based on available space
    currentDirection = autonomousRobot.GetFurthestEnd()

    # if we have less than 10 cm left in our preferred direction see if another direction would be better
    while currentDirection[1] < 20.0:
        autonomousRobot.RotateToBiggestSpace()
        currentDirection = autonomousRobot.GetFurthestEnd()

    autonomousRobot.SetSpeedBasedOnDistance(currentDirection[1])
    autonomousRobot.robot.Move(currentDirection[0])
    loop = 1

    while True:
        currentDirection = autonomousRobot.GetDistanceToNextObstacle()
            
        loop -= 1
        if loop == 0:
            loop = 4
            print(currentDirection)

        # adjust speed as we get closer to a barrier
        autonomousRobot.SetSpeedBasedOnDistance(currentDirection[1])

        # change direction if there is less than 10cm left in direction of travel  
        if currentDirection[1] < 25.0 or autonomousRobot.AreWeStuck(currentDirection[0], currentDirection[1]): 
            print("spinning", currentDirection)
            currentDirection = autonomousRobot.RotateToBiggestSpace()
            autonomousRobot.SetSpeedBasedOnDistance(currentDirection[1])
            autonomousRobot.robot.Move(currentDirection[0])

        autonomousRobot.UpdatePosition(currentDirection[0], currentDirection[1])
        time.sleep(0.6)

except KeyboardInterrupt:
    autonomousRobot.robot.Stop()
finally:
    autonomousRobot.robot.Stop()
    autonomousRobot.sensors.StopScanner()
    GPIO.cleanup()