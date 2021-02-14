from gpiozero import Button
from gpiozero import LED
from time import sleep

button = Button(18)
led = LED(17)
buttonState = False

while True:
    if button.is_pressed:
        buttonState = True
    else:
        buttonState = False
    if buttonState:
        led.on()
    else:
        led.off()
