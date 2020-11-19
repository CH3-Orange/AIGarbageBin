import RPi.GPIO as GPIO
import time
from gpiozero import MotionSensor,LED

led=LED(19)
sensIO=12
time_out=1
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensIO,GPIO.IN)

try:
    while True:
        if(GPIO.input(sensIO)==True):
            print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"!!")
            led.on()
        else:
            print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"no")
            led.off()
        time.sleep(time_out)
        
except keyboardInterrupt:
    pass
GPIO.cleanup()