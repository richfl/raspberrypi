import sys
import time
import RPi.GPIO as GPIO

#mode=GPIO.getmode()
#GPIO.cleanup()
FlForward=16
FlBackward=15
FrForward=22
FrBackward=18
BrForward=8
BrBackward=33
BlForward=13
BlBackward=10

Direction = 's'
Speed = 80
Frequency = 1000
try:
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(FlBackward, GPIO.OUT)
    GPIO.setup(FlForward, GPIO.OUT)
    GPIO.setup(FrForward, GPIO.OUT)f
    GPIO.setup(FrBackward, GPIO.OUT)
    GPIO.setup(BlForward, GPIO.OUT)
    GPIO.setup(BlBackward, GPIO.OUT)
    GPIO.setup(BrForward, GPIO.OUT)
    GPIO.setup(BrBackward, GPIO.OUT)
    flfpwm = GPIO.PWM(FlForward, Frequency)
    flbpwm = GPIO.PWM(FlBackward, Frequency)
    frfpwm = GPIO.PWM(FrForward, Frequency)
    frbpwm = GPIO.PWM(FrBackward, Frequency)
    blfpwm = GPIO.PWM(BlForward, Frequency)
    blbpwm = GPIO.PWM(BlBackward, Frequency)
    brfpwm = GPIO.PWM(BrForward, Frequency)
    brbpwm = GPIO.PWM(BrBackward, Frequency)

    def flforward():
        flfpwm.start(Speed)

    def flreverse():
        flbpwm.start(Speed)

    def frforward():
        frfpwm.start(Speed)

    def frreverse():
        frbpwm.start(Speed)

    def blforward():
        blfpwm.start(Speed)

    def blreverse():
        blbpwm.start(Speed)

    def brforward():
        brfpwm.start(Speed)

    def brreverse():
        brbpwm.start(Speed)

    def stop():
        global Direction
        Direction = 's'
        print('Stopping')
        flfpwm.stop()
        flbpwm.stop()
        frfpwm.stop()
        frbpwm.stop()
        blfpwm.stop()
        blbpwm.stop()
        brfpwm.stop()
        brbpwm.stop()

    def AllForward():
        global Direction
        if (Direction != 'f'):
            stop()
            Direction = 'f'
        flforward()
        frforward()
        blforward()
        brforward()

    def AllBackward():
        global Direction
        if (Direction != 'b'):
            stop()
            Direction = 'b'
        flreverse()
        frreverse()
        blreverse()
        brreverse()    

    def SpinRight():
        global Direction
        if (Direction != 'r'):
            stop()
            Direction = 'r'
        flforward()
        blforward()
        frreverse()
        brreverse()

    def SpinLeft():
        global Direction
        if (Direction != 'l'):
            stop()
            Direction = 'l'
        frforward()
        brforward()
        flreverse()
        blreverse()

    def MoveRight():
        global Direction
        if (Direction != 'mr'):
            stop()
            Direction = 'mr'
        frreverse()
        brforward()
        flforward()
        blreverse()

    def MoveLeft():
        global Direction
        if (Direction != 'ml'):
            stop()
            Direction = 'ml'
        frforward()
        brreverse()
        flreverse()
        blforward()

    stop()
    x = 's'
    while (x != 'e'):
        x=input()

        if x =='f':
            AllForward()
        elif x == 'b':
            AllBackward()
        elif x == 's' or x == '0':
            stop()
        elif x == 'l':
            SpinLeft()
        elif x == 'r':
            SpinRight()
        elif x == 'mr':
            MoveRight()
        elif x == 'ml':
            MoveLeft()
        elif x >= '4' and x <= '9':
            Speed = int(x) * 10
        elif x > '0' and x <= '3':
            Speed = 100
finally:
    GPIO.cleanup()