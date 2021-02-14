from gpiozero import Robot
from time import sleep

robby = Robot(left=(11,9), right=(13,10))

speed = 1.0
turnspeed = 0.8
robby.forward(speed)
print("forward")
sleep(3)
robby.right(turnspeed)
print("right")
sleep(3)
robby.forward(speed)
print("forward")
sleep(3)
robby.left(turnspeed)
print("left")
sleep(3)
print("Stop")
robby.stop()
