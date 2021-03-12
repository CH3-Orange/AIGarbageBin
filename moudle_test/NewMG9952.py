from gpiozero import Servo
from time import sleep
import  numpy as np
myGPIO=[14,15,18,23]
ResetVal=[-0.5,0.4,-0.5,0.3]
DownVal=[-1,1,-1,1]
UpVal=[-0.6,0.5,-0.6,0.4]
Sers=[]

    
def STurn(ser,num):
    ser.value=num
    sleep(1)
    ser.detach()
def SSTurn(ser,num):
    ser.value=-1
    sleep(3)
    for i in np.arange(-1,num+0.08,0.1):
        ser.value=i
        print(i)
        sleep(0.3)
def ResetSers():
    for i in range(4):
        STurn(Sers[i],ResetVal[i])
def DownSers():
    for i in range(4):
        STurn(Sers[i],DownVal[i])
def main():
    
    myCorrection=0.40
    maxPW=(2.0+myCorrection)/1000
    minPW=(1.0-myCorrection)/1000
    servo0 = Servo(myGPIO[0],min_pulse_width=minPW,max_pulse_width=maxPW)
    servo1 = Servo(myGPIO[1],min_pulse_width=minPW,max_pulse_width=maxPW)
    servo2 = Servo(myGPIO[2],min_pulse_width=minPW,max_pulse_width=maxPW)
    servo3 = Servo(myGPIO[3],min_pulse_width=minPW,max_pulse_width=maxPW)
    servo0.detach()
    servo1.detach()
    servo2.detach()
    servo3.detach()
    Sers.append(servo0)
    Sers.append(servo1)
    Sers.append(servo2)
    Sers.append(servo3)
    #STurn(Sers[3],0.5)
    ResetSers()
    DownSers()
#     ResetSers()
#     while True:
#         inp=input()
#         inp2=input()
#         print((eval(inp),eval(inp2)))
#         STurn(Sers[eval(inp)],eval(inp2))
#         print(Sers[eval(inp)].value)
    
main()


