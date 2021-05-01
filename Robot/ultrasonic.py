import RPi.GPIO as GPIO
import time
import threading
from servos import Servos, ServoEnd, ServoDirection

class DistanceSensors:

    def __init__(self):
        self.GPIO_FRONTTRIGGER = 20
        self.GPIO_BACKTRIGGER = 5
        self.GPIO_FRONTECHO = 6
        self.GPIO_BACKECHO = 12

        FRONTSERVO = 6
        BACKSERVO = 7

        #set GPIO direction (IN / OUT)
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_FRONTECHO, GPIO.IN)
        GPIO.setup(self.GPIO_BACKECHO, GPIO.IN)
        GPIO.setup(self.GPIO_FRONTTRIGGER, GPIO.OUT)
        GPIO.output(self.GPIO_FRONTTRIGGER, False)
        GPIO.setup(self.GPIO_BACKTRIGGER, GPIO.OUT)
        GPIO.output(self.GPIO_BACKTRIGGER, False)

        # initialise direction servos
        self.servos = Servos(FRONTSERVO, BACKSERVO)
        servoPositions = self.servos.FirstScanPosition()
        self.frontServoDirection = servoPositions[0]
        self.backServoDirection = servoPositions[1]
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
        time.sleep(1)

    # threaded function
    def GetDistance(self, delay):
        while not(self.endthread):
            frontError = backError = False

            # Activate echo trigger (this is shared between front and rear sensors)
            GPIO.output(self.GPIO_FRONTTRIGGER, True)
            time.sleep(0.00001)
            GPIO.output(self.GPIO_FRONTTRIGGER, False)

            frontStartTime = frontStopTime = time.time()
            while GPIO.input(self.GPIO_FRONTECHO) == 0:
                frontStartTime = time.time()
                if frontStartTime - frontStopTime > 0.02:
                    frontError = True
                    break
            while GPIO.input(self.GPIO_FRONTECHO) == 1 and not(frontError):
                frontStopTime = time.time()
                if frontStopTime - frontStartTime > 0.02:
                    frontError = True
                    break
            time.sleep(0.08)

            # Activate echo trigger (this is shared between front and rear sensors)
            GPIO.output(self.GPIO_BACKTRIGGER, True)
            time.sleep(0.00001)
            GPIO.output(self.GPIO_BACKTRIGGER, False)
            
            backStartTime = backStopTime = time.time()
            while GPIO.input(self.GPIO_BACKECHO) == 0:
                backStartTime = time.time()
                if backStartTime - backStopTime > 0.02:
                    backError = True
                    break
            while GPIO.input(self.GPIO_BACKECHO) == 1 and not (backError):
                backStopTime = time.time()
                if backStopTime - backStartTime > 0.02:
                    backError = True
                    break

            # time difference between start and return
            frontdistance = (frontStopTime - frontStartTime) * 17150
            backdistance = (backStopTime - backStartTime) * 17150

            if frontdistance > 0 and not(frontError):
                self.frontDistance[self.frontServoDirection] = frontdistance
            if backdistance> 0 and not(backError):
                self.backDistance[self.backServoDirection] = backdistance

            # move servos to next direction to scan
            servoDirections = self.servos.NextScanPosition()
            self.frontServoDirection = servoDirections[0]
            self.backServoDirection = servoDirections[1]
            time.sleep(delay)

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
                    if self.frontDistance[key] == -1.0:
                        done = False
                for key in self.backDistance:
                    if self.backDistance[key] == -1.0:
                        done = False
                attempts -= 1
            return done
        else:
            return True

    def StopScanner(self):
        self.endthread = True
        self.ultrathread.join()
        self.scannerActive = False

# try:
#     sensors = DistanceSensors()
#     sensors.StartScanner(0.1, True)
#     while sensors.scannerActive:
#         # if keyboard.read_key() == 'e':
#         #     sensors.StopScanner()
       
#         print("Front")
#         print(sensors.frontDistance)
#         print("back")
#         print(sensors.backDistance)
#         time.sleep(1)
#      # Reset by pressing CTRL + C
# except KeyboardInterrupt:
#     sensors.StopScanner()
# finally:
#     GPIO.cleanup()