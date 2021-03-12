from gpiozero import Servo
from time import sleep
myGPIO=[14,23,17,18]
ResetVal=[0.4,-0.15,0.5,0.55]
DownVal=[1,-0.7,1,1]
UpVal=[0.3,0,0.3,0.4]
Sers=[]

def STurn(ser,num):
    ser.value=num
    sleep(1)
    ser.detach()

def ResetSers():
    for i in range(4):
        STurn(Sers[i],ResetVal[i])
def DownSers():
    for i in range(4):
        STurn(Sers[i],DownSers[i])
def main():
    
    myCorrection=0.40
    maxPW=(2.0+myCorrection)/1000
    minPW=(1.0-myCorrection)/1000
    servo0 = Servo(myGPIO[0],min_pulse_width=minPW,max_pulse_width=maxPW)
    servo1 = Servo(myGPIO[1],min_pulse_width=minPW,max_pulse_width=maxPW)
    servo2 = Servo(myGPIO[2],min_pulse_width=minPW,max_pulse_width=maxPW)
    servo3 = Servo(myGPIO[3],min_pulse_width=minPW,max_pulse_width=maxPW)
    Sers.append(servo0)
    ResetSers()
    DownSers()
    ResetSers()
    



