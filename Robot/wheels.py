import sys
import RPi.GPIO as GPIO
import wheel

mode = GPIO.getmode()
GPIO.cleanup()

Direction = 's'
Speed = 80
Frequency = 1000

GPIO.setmode(GPIO.BOARD)

wheels = {}

wheels['fl'] = wheel(16, 15, Speed, Frequency)
wheels['fr'] = wheel(22, 18, Speed, Frequency)
wheels['bl'] = wheel(13, 10, Speed, Frequency)
wheels['br'] = wheel(8, 33, Speed, Frequency)

def stop():
    wheels['fl'].stop()
    wheels['fr'].stop()
    wheels['bl'].stop()
    wheels['br'].stop()

def AllForward():
    global Direction
    if (Direction != 'f'):
        stop()
        Direction = 'f'
        wheels['fl'].forward()
        wheels['fr'].forward()
        wheels['br'].forward()
        wheels['bl'].forward()

def AllBackward():
    global Direction
    if (Direction != 'b'):
        stop()
        Direction = 'b'
        wheels['fl'].reverse()
        wheels['fr'].reverse()
        wheels['br'].reverse()
        wheels['bl'].reverse()

def SpinRight():
    global Direction
    if (Direction != 'r'):
        stop()
        Direction = 'r'
        wheels['fl'].forward()
        wheels['fr'].reverse()
        wheels['br'].reverse()
        wheels['bl'].forward()

def SpinLeft():
    global Direction
    if (Direction != 'l'):
        stop()
        Direction = 'l'
        wheels['fl'].reverse()
        wheels['fr'].forward()
        wheels['br'].forward()
        wheels['bl'].reverse()

def MoveRight():
    global Direction
    if (Direction != 'mr'):
        stop()
        Direction = 'mr'
        wheels['fl'].forward()
        wheels['fr'].reverse()
        wheels['br'].forward()
        wheels['bl'].reverse()

def MoveLeft():
    global Direction
    if (Direction != 'ml'):
        stop()
        Direction = 'ml'
        wheels['fl'].reverse()
        wheels['fr'].forward()
        wheels['br'].reverse()
        wheels['bl'].forward()

def Speed(newspeed):
    global Speed
    if (Speed != newspeed)
        wheels['fl'].setspeed(newspeed)
        wheels['fr'].setspeed(newspeed)
        wheels['bl'].setspeed(newspeed)
        wheels['br'].setspeed(newspeed)

stop()
x = Direction

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
        Speed(int(x) * 10)
    elif x > '0' and x <= '3':
        Speed(100)

GPIO.cleanup()