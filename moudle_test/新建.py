from gpiozero import Servo
from time import sleep

def STurn(ser,num):
    ser.value=float(num)
    sleep(1)
    ser.detach()

myGPIO=[14,15,17,18]
ResetVal=[0.4,-0.15,0.5,0.55]
DownVal=[1,-0.7,1,1]
UpVal=[0.3,0,0.3,0.4]
myCorrection=0.40
maxPW=(2.0+myCorrection)/1000
minPW=(1.0-myCorrection)/1000

servo0 = Servo(myGPIO[0],min_pulse_width=minPW,max_pulse_width=maxPW)
servo1 = Servo(myGPIO[1],min_pulse_width=minPW,max_pulse_width=maxPW)
servo2 = Servo(myGPIO[2],min_pulse_width=minPW,max_pulse_width=maxPW)
servo3 = Servo(myGPIO[3],min_pulse_width=minPW,max_pulse_width=maxPW)
Sers=[servo0,servo1,servo2,servo3]

servo0.detach()
servo1.detach()
servo2.detach()
servo3.detach()
#servo.mid()

#servo0.value=0.4
#for i in range(4):
#    STurn(Sers[i],ResetVal[i])
STurn(Sers[3],ResetVal[3])
#servo2.value=0.5
#servo3.value=0.55
sleep(0.5)
servo0.detach()
servo1.detach()
servo2.detach()
servo3.detach()
sleep(3)

#servo0.value=1
#sleep(0.5)
#servo0.detach()
#sleep(2)
#servo1.value=0
#sleep(0.5)
#servo1.value=-0.15
#servo1.detach()



