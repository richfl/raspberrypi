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

        self.HistoryFront = [[0.0, 0.0, 0.0, 0.0, 0.0]]
        self.HistoryBack = [[0.0, 0.0, 0.0, 0.0, 0.0]]
        self.FrontDeltas = [[0.0, 0.0, 0.0, 0.0, 0.0]]
        self.BackDeltas = [[0.0, 0.0, 0.0, 0.0, 0.0]]
        self.FrontDeltaDelta = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.BackDeltaDelta = [0.0, 0.0, 0.0, 0.0, 0.0]

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

    def UpdateStatistics(self):
        if len(self.HistoryFront) == 1:
            self.HistoryFront = [[self.frontDistance[ServoDirection.Left],
                            self.frontDistance[ServoDirection.OffLeft],
                            self.frontDistance[ServoDirection.Ahead],
                            self.frontDistance[ServoDirection.OffRight],
                            self.frontDistance[ServoDirection.Right]]]
            self.HistoryBack = [[self.backDistance[ServoDirection.Left],
                            self.backDistance[ServoDirection.OffLeft],
                            self.backDistance[ServoDirection.Ahead],
                            self.backDistance[ServoDirection.OffRight],
                            self.backDistance[ServoDirection.Right]]]

        self.HistoryFront += [[self.frontDistance[ServoDirection.Left],
                            self.frontDistance[ServoDirection.OffLeft],
                            self.frontDistance[ServoDirection.Ahead],
                            self.frontDistance[ServoDirection.OffRight],
                            self.frontDistance[ServoDirection.Right]]]
        self.HistoryBack += [[self.backDistance[ServoDirection.Left],
                            self.backDistance[ServoDirection.OffLeft],
                            self.backDistance[ServoDirection.Ahead],
                            self.backDistance[ServoDirection.OffRight],
                            self.backDistance[ServoDirection.Right]]]

        self.FrontDeltas += [[round(self.HistoryFront[-1][0] - self.HistoryFront[-2][0], 1),
                            round(self.HistoryFront[-1][1] - self.HistoryFront[-2][1], 1),
                            round(self.HistoryFront[-1][2] - self.HistoryFront[-2][2], 1),
                            round(self.HistoryFront[-1][3] - self.HistoryFront[-2][3], 1),
                            round(self.HistoryFront[-1][4] - self.HistoryFront[-2][4], 1)]]
            
        self.BackDeltas += [[round(self.HistoryBack[-1][0] - self.HistoryBack[-2][0], 1),
                            round(self.HistoryBack[-1][1] - self.HistoryBack[-2][1], 1),
                            round(self.HistoryBack[-1][2] - self.HistoryBack[-2][2], 1),
                            round(self.HistoryBack[-1][3] - self.HistoryBack[-2][3], 1),
                            round(self.HistoryBack[-1][4] - self.HistoryBack[-2][4], 1)]]
        # only keep the most recent 10 entries
        if (len(self.HistoryFront) > 10):
            del self.HistoryFront[0]
            del self.HistoryBack[0]
            del self.FrontDeltas[0]
            del self.BackDeltas[0]
        
        self.FrontDeltaDelta = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.BackDeltaDelta = [0.0, 0.0, 0.0, 0.0, 0.0]

        for j in range(0, min(5, len(self.FrontDeltas))):
            for i in range(0, 4):
                self.FrontDeltaDelta[i] += self.FrontDeltas[j][i]
                self.BackDeltaDelta[i] += self.BackDeltas[j][i]
                
        for i in range(0, 4):
            self.FrontDeltaDelta[i] = round(self.FrontDeltaDelta[i], 1)
            self.BackDeltaDelta[i] = round(self.BackDeltaDelta[i], 1)

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

            if (self.frontServoDirection == ServoDirection.Left):
                self.UpdateStatistics()

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

try:
    sensors = DistanceSensors()
    sensors.StartScanner(0.1, True)
    while sensors.scannerActive:
        # if keyboard.read_key() == 'e':
        #     sensors.StopScanner()
       
        # print("Front")
        # print(sensors.frontDistance)
        # print("back")
        # print(sensors.backDistance)
        time.sleep(1)
        print("Back", sensors.BackDeltaDelta, sensors.BackDeltas[-1])
        print("Front", sensors.FrontDeltaDelta, sensors.FrontDeltas[-1])
     # Reset by pressing CTRL + C
except KeyboardInterrupt:
    sensors.StopScanner()
finally:
    GPIO.cleanup()