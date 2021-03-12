from gpiozero import LED
import time

Led=LED(1)
Led.on()
time.sleep(1)
Led.off()