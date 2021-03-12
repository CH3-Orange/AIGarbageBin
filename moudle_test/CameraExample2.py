from picamera import PiC
from time import sleep

camera=Pic()

camera.start_preview()
sleep(5)
camera.stop_preview()