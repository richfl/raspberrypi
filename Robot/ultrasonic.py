import RPi.GPIO as GPIO
import time
import threading
import keyboard

# TODO
# run two sensors (front/back - make both use the same trigger)
# https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi

GPIO.setmode(GPIO.BOARD)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

frontdistance = float(-1.0)
endthread = False

def Distance():
    global frontdistance # assume writing to an int is an atomic operation
    global endthread

    while not(endthread):
        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
    
        StartTime = time.time()
        StopTime = time.time()
    
        # save StartTime
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
    
        # save time of arrival
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
    
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime

        # multiply with the sonic speed (34300 cm/s) and divide by 2, because there and back
        frontdistance = TimeElapsed * 17150
 
try:
    ultrathread = threading.Thread(target=Distance, args=(1,))
    print("Main    : before running thread")
    ultrathread.start()

    while not(endthread):
        if keyboard.read_key() == 'e':
            endthread = True
        print("Measured Distance = %.1f cm" % frontdistance)
        time.sleep(1)

    # Reset by pressing CTRL + C
except KeyboardInterrupt:
    endthread = True
    print("Main    : wait for the thread to finish")
    x.join()
    print("Main    : all done")
    print("Measurement stopped by User")
    GPIO.cleanup()