from gpiozero import Servo,Button
from time import sleep

btn=Button(3)
while True:
    if btn.is_pressed:
        print("ON")
    else:
        print("OFF")
    sleep(1)
