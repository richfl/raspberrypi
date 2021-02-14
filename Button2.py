from gpiozero import Button, PWMLED
from signal import pause


def say_hello():
    led.pulse()

def say_goodbye():
    led.off()

button = Button(18)
led = PWMLED(17)

button.when_pressed = say_hello
button.when_released = say_goodbye

pause()