import os, sys
import math
import time
 
import busio
import board
 
import numpy as np
import pygame, evdev, time
from scipy.interpolate import griddata
 
from colour import Color
 
import adafruit_amg88xx
import adafruit_vl53l0x
 
i2c_bus = busio.I2C(board.SCL, board.SDA)
 
#low range of the sensor (this will be blue on the screen)
MINTEMP = 16.
 
#high range of the sensor (this will be red on the screen)
MAXTEMP = 25.
 
#how many color values we can have
COLORDEPTH = 2048

surfaceSize = (320, 240)

#os.putenv('SDL_FBDEV', '/dev/fb0')
pygame.init()
# displayInfo = pygame.display.get_wm_info()

lcd = pygame.Surface(surfaceSize)

# This is the important bit
def refresh():
    # We open the TFT screen's framebuffer as a binary file. Note that we will write bytes into it, hence the "wb" operator
    f = open("/dev/fb1","wb")
    # According to the TFT screen specs, it supports only 16bits pixels depth
    # Pygame surfaces use 24bits pixels depth by default, but the surface itself provides a very handy method to convert it.
    # once converted, we write the full byte buffer of the pygame surface into the TFT screen framebuffer like we would in a plain file:
    f.write(lcd.convert(16,0).get_buffer())
    # We can then close our access to the framebuffer
    f.close()
    #time.sleep(0.1)

# Now we've got a function that can get the bytes from a pygame surface to the TFT framebuffer, 
# we can use the usual pygame primitives to draw on our surface before calling the refresh function.

# Here we just blink the screen background in a few colors with the "Hello World!" text
pygame.font.init()
defaultFont = pygame.font.SysFont(None,30)

#initialize the sensor
sensor = adafruit_amg88xx.AMG88XX(i2c_bus)
laserRange = adafruit_vl53l0x.VL53L0X(i2c_bus)

# pylint: disable=invalid-slice-index
points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]
# pylint: enable=invalid-slice-index
 
#sensor is an 8x8 grid so lets do a square
height = 240
width = 240
 
#the list of colors we can choose from
blue = Color("indigo")
colors = list(blue.range_to(Color("red"), COLORDEPTH))
 
#create the array of colors
colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]
 
displayPixelWidth = width / 30
displayPixelHeight = height / 30
 
pygame.mouse.set_visible(False)
lcd.fill((0, 0, 0))
refresh()
 
#some utility functions
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))
 
def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
 
#let the sensor initialize
#time.sleep(.1)
 
while True:
    try:
        timer = time.perf_counter_ns()
        
        #print(f"Range: {(laserRange.range - 57) / 10}cm")
        time.sleep(0.05)
        #read the pixels
        pixels = []
        for row in sensor.pixels:
            pixels = pixels + row
        pixels = [map_value(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]
    
        #perform interpolation
        bicubic = griddata(points, pixels, (grid_x, grid_y), method='cubic')
    
        #draw everything
        for ix, row in enumerate(bicubic):
            for jx, pixel in enumerate(row):
                pygame.draw.rect(lcd, colors[constrain(int(pixel), 0, COLORDEPTH- 1)],
                                (displayPixelHeight * ix, displayPixelWidth * jx,
                                displayPixelHeight, displayPixelWidth))
        lcd.blit(defaultFont.render(f"{(laserRange.range - 57) / 10}cm", False, (0, 0, 0)),(0, 0))
        refresh()
        print (f"processing time {(time.perf_counter_ns() - timer)/1000000}ms. temp {sensor.temperature}")
    except:
        print (f"Error {sys.exc_info()[0]} {sys.exc_info()[1]}")
