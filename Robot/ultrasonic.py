import RPi.GPIO as GPIO
import time
import threading
from servos import Servos, ServoEnd, ServoDirection

class DistanceSensors:

    def __init__(self):
        self.GPIO_TRIGGER = 20
        self.GPIO_FRONTECHO = 6
        self.GPIO_BACKECHO = 12

        FRONTSERVO = 6
        BACKSERVO = 7

        #set GPIO direction (IN / OUT)
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_FRONTECHO, GPIO.IN)
        GPIO.setup(self.GPIO_BACKECHO, GPIO.IN)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.output(self.GPIO_TRIGGER, False)
        time.sleep(1)

        # initialise direction servos
        self.servos = Servos(FRONTSERVO, BACKSERVO)
        self.servoDirection = self.servos.FirstScanPosition()
        self.scannerActive = False
        self.endthread = False

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

    def StartScanner(self, delay, getFirstScan = False):
        self.endthread = False
        self.ultrathread = threading.Thread(target=self.GetDistance, args=(delay,))
        self.ultrathread.start()
        self.scannerActive = True
        if getFirstScan:
            done = False
            attempts = 3
            while not(done) and attempts > 0:
                time.sleep(delay * 5)
                done = True
                for key in self.frontDistance:
                    if in self.frontDistance[key] == -1.0:
                        done = False
                for key in self.backDistance:
                    if in self.backDistance[key] == -1.0:
                        done = False
                attempts--
            return done
        else
            return True

    def StopScanner(self):
        self.endthread = True
        self.ultrathread.join()
        self.scannerActive = False

    # threaded function
    def GetDistance(self, delay):
        while not(self.endthread):
            frontEcho = True
            backEcho = True
            frontEchoActive = False
            backEchoActive = False
            frontStartTime = time.time()
            frontStopTime = frontStartTime
            backStartTime = frontStartTime
            backStopTime = frontStartTime

            # Activate echo trigger (this is shared between front and rear sensors)
            GPIO.output(self.GPIO_TRIGGER, True)
            time.sleep(0.00001)
            GPIO.output(self.GPIO_TRIGGER, False)

            # Get current front and back distances
            while frontEcho or backEcho:
                if GPIO.input(self.GPIO_FRONTECHO) == 0 and frontEchoActive:
                    frontEcho = False
                elif GPIO.input(self.GPIO_FRONTECHO) == 0 and frontEcho:
                    frontStartTime = time.time()
                elif GPIO.input(self.GPIO_FRONTECHO) == 1:
                    frontEchoActive = True
                    frontStopTime = time.time()

                if GPIO.input(self.GPIO_BACKECHO) == 0 and backEchoActive:
                    backEcho = False
                elif GPIO.input(self.GPIO_BACKECHO) == 0 and backEcho:
                    backStartTime = time.time()
                elif GPIO.input(self.GPIO_BACKECHO) == 1:
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
            time.sleep(delay)


# try:
#     sensors = DistanceSensors()
#     sensors.StartScanner(0.5)

#     while sensors.scannerActive:
#         # if keyboard.read_key() == 'e':
#         #     sensors.StopScanner()
        
#         print("Front")
#         print(sensors.frontDistance)
#         print("back")
#         print(sensors.backDistance)
#         time.sleep(1)

#     # Reset by pressing CTRL + C
# except KeyboardInterrupt:
#     sensors.StopScanner()
#     GPIO.cleanup()
# finally:
#     GPIO.cleanup()