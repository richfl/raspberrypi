import RPi.GPIO as GPIO
import time
import threading
import keyboard
from servos import Servos, ServoEnd, ServoDirection

# TODO
# run two sensors (front/back - make both use the same trigger)
# https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi

class DistanceSensors(self):
    GPIO_TRIGGER = 37
    GPIO_FRONTECHO = 32
    GPIO_BACKECHO = 31

    FRONTSERVO = 6
    BACKSERVO = 7

    def __init__(self)
         # initialise direction servos
        self.servos = Servos(FRONTSERVO, BACKSERVO)
        self.servoDirection = self.servos.FirstScanPosition()
        self.scannerActive = False

        self.endthread = False
        
        #set GPIO direction (IN / OUT)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_FRONTECHO, GPIO.IN)
        GPIO.setup(GPIO_BACKECHO, GPIO.IN)

        # initialise current distance readings
        self.frontDistance = {
            ServoDirection.Left: -1.0,
            ServoDirection.OffLeft: -1.0,
            ServoDirection.Ahead: -1.0,
            ServoDirection.OffRight: -1.0,
            ServoDirection.Right: -1.0
        }

        self.backDistance = {
            ServoDirection.Left: -1.0,
            ServoDirection.OffLeft: -1.0,
            ServoDirection.Ahead: -1.0,
            ServoDirection.OffRight: -1.0,
            ServoDirection.Right: -1.0
        }

        self.ultrathread = threading.Thread(target=self.GetDistance, args=(1,))

    def StartScanner(self):
        self.endthread = False
        self.ultrathread.start()
        self.scannerActive = True

    def StopScanner(self):
        self.endthread = True
        thread.join(self.ultrathread)
        self.scannerActive = False

    # threaded function
    def GetDistance(self):
        while not(self.endthread):
            frontEcho = True
            backEcho = True
            frontEchoActive = False
            backEchoActive = False
            FrontStartTime = time.time()
            FrontStopTime = FrontStartTime
            BackStartTime = FrontStartTime
            BackStopTime = FrontStartTime

            # Activate echo trigger (this is shared between front and rear sensors)
            GPIO.output(GPIO_TRIGGER, True)
            time.sleep(0.00001)
            GPIO.output(GPIO_TRIGGER, False)

            # Get current front and back distances
            while frontEcho or backEcho:
                if GPIO.input(GPIO_FRONTECHO) == 0 and frontEchoActive:
                    frontEcho = False
                elif GPIO.input(GPIO_FRONTECHO) == 0 and frontEcho:
                    FrontStartTime = time.time()
                elif GPIO.input(GPIO_FRONTECHO) == 1:
                    frontEchoActive = True
                    frontStopTime = time.time()

                if GPIO.input(GPIO_BACKECHO) == 0 and backEchoActive:
                    backEcho = False
                elif GPIO.input(GPIO_BACKECHO) == 0 and backEcho:
                    BackStartTime = time.time()
                elif GPIO.input(GPIO_BACKECHO) == 1:
                    backEchoActive = True
                    backStopTime = time.time()

            # time difference between start and return
            frontdistance = (frontStopTime - frontStartTime) * 17150
            backdistance = (backStopTime - backStartTime) * 17150

            # save front and back distance for current servo direction
            self.frontDistance[self.servoDirection] = frontdistance
            self.backDistance[self.servoDirection] = backdistance

            # move servos to next direction to scan
            self.servoDirection = self.servos.NextScanPosition()


try:
    sensors = DistanceSensors()
    sensors.StartScanner()

    while sensors.scannerActive:
        if keyboard.read_key() == 'e':
            sensors.StopScanner()
        
        print("Front" + sensors.frontDistance)
        print("back" + sensors.backDistance)
        time.sleep(1)

    # Reset by pressing CTRL + C
except KeyboardInterrupt:
    sensors.StopScanner()
    GPIO.cleanup()
finally:
    GPIO.cleanup()