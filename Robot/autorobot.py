import sys
import RPi.GPIO as GPIO
from wheels import Wheels, Direction
from ultrasonic import DistanceSensors
from servos import ServoDirection, ServoEnd

sensors = DistanceSensors()
robot = Wheels()

def GetDistanceToNextObstacle():
    distance = -1.0
    if robot.Direction == Direction.Forward or robot.Direction == Direction.Stop 
        or robot.Direction == Direction.SpinLeft or robot.Direction == Direction.SpinRight:
        distance = sensors.frontDistance[ServoDirection.Ahead]
    elif robot.Direction == Direction.Reverse:
        distance = sensors.backDistance[ServoDirection.Ahead]
    elif robot.Direction == Direction.ForwardRight:
        distance = sensors.frontDistance[ServoDirection.OffRight]
    elif robot.Direction == Direction.ForwardLeft:
        distance = sensors.frontDistance[ServoDirection.OffLeft]
    elif robot.Direction == Direction.ReverseLeft:
        distance = sensors.backDistance[ServoDirection.OffLeft]
    elif robot.Direction == Direction.ReverseRight:
        distance = sensors.backDistance[ServoDirection.OffRight]
    elif robot.Direction == Direction.MoveRight:
        distance = sensors.frontDistance[ServoDirection.Right]
    elif robot.Direction == Direction.MoveLeft:
        distance = sensors.frontDistance[ServoDirection.Left]
    return distance

def GetFurthestEnd()
# just work out if there is more space infront or behind and ignore sides
    if sensors.backDistance[ServoDirection.Ahead] > sensors.frontDistance[ServoDirection.Ahead]:
        return (Direction.Reverse, sensors.backDistance[ServoDirection.Ahead])
    else:
        return (Direction.Forward, sensors.frontDistance[ServoDirection.Ahead])

def GetMaxDistanceDirection()
# returns the sensor direction with the most space and what that distance is
    maxRearDistance = max(sensors.backDistance.values())
    maxFrontDistance = max(sensors.frontDistance.values())

    if maxRearDistance > maxFrontDistance:
        res = [key for key in sensors.backDistance if sensors.backDistance[key] == maxRearDistance]
        return (ServoEnd.Back, res[0], maxRearDistance)
    else:
        res = [key for key in sensors.frontDistance if sensors.frontDistance[key] == maxFrontDistance]
        return (ServoEnd.Front, res[0], maxFrontDistance)

def GetMinDistanceDirection()
# returns the sensor direction with the least space and what that distance is
    minRearDistance = min(sensors.backDistance.values())
    minFrontDistance = min(sensors.frontDistance.values())

    if minRearDistance < minFrontDistance:
        res = [key for key in sensors.backDistance if sensors.backDistance[key] == minRearDistance]
        return (ServoEnd.Back, res[0], minRearDistance)
    else:
        res = [key for key in sensors.frontDistance if sensors.frontDistance[key] == minFrontDistance]
        return (ServoEnd.Front, res[0], minFrontDistance)

def SetSpeedBasedOnDistance(distance):
    if distance < 5.0:
        robot.Stop()
    elif distance < 10.0:
        robot.SetSpeed(4)
    elif distance < 20.0:
        robot.SetSpeed(6) 
    elif distance < 30.0:
        robot.SetSpeed(8) 
    else:
        robot.SetSpeed(10) 
    return robot.robotspeed

def RotateToBiggestSpace()
# rotates so either front or rear is pointing to biggests space.
# returns whether forwards or reverse is best and how much space there is in that direction
    while True # repeat until the front or back is pointing to the biggest space)
        preferredDirection = GetMaxDistanceDirection()

        # if the best direction is forward or reverse don't spin and return
        if preferredDirection[1] == ServoDirection.Ahead:
            if preferredDirection[0] == ServoEnd.Front:
                return Direction.Forward, preferredDirection[2]
            else:
                return Direction.Reverse, preferredDirection[2]
        
        # work out whether to spin right or left
        if (preferredDirection[0] == ServoEnd.Front and 
            (preferredDirection[1] == ServoDirection.OffRight or preferredDirection[1] == ServoDirection.Right))
            or
            (preferredDirection[0] == ServoEnd.Back and 
            (preferredDirection[1] == ServoDirection.OffLeft or preferredDirection[1] == ServoDirection.Left)):
            robot.SpinRight()
        else
            robot.SpinLeft()

        if ServoDirection.OffLeft or ServoDirection.OffRight:
            time.Sleep(0.5) # rotate 45 degrees
        else: 
            time.Sleep(1) # rotate 90 degrees
        robot.Stop()

        # wait to get new set of distance readings - worst case is potentially 4 seconds
        time.sleep(3)


try:
    robot.Stop()
    # Determine space around robot and find biggest open space
    if not(sensors.StartScanner(0.5, True)):
        raise "Distance sensors not working"

    # work out if we want to go forwards or backwards based on available space
    currentDirection = GetFurthestEnd()
    if currentDirection[1] < 30.0:
        # if we have less than 30 cm left in our preferred direction see if another direction would be better
        RotateToBiggestSpace()
        currentDirection = GetFurthestEnd()
    SetSpeedBasedOnDistance(currentDirection[1])
    robot.Move(currentDirection[0])
  
    while true:
        # adjust speed as we get closer to a barrier
        SetSpeedBasedOnDistance(GetDistanceToNextObstacle())

        if GetDistanceToNextObstacle() < 10.0: 
            # change direction if there is less than 10cm left in direction of travel
            newDirection = RotateToBiggestSpace()
            currentDirection = newDirection[0]
            SetSpeedBasedOnDistance(GetDistanceToNextObstacle())
            robot.Move(currentDirection)

finally:
    sensors.StopScanner()
    robot.Stop()
    GPIO.cleanup()