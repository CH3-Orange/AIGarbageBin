import ENV
import time
if ENV.__ENV__=="RaspberryPi":
    from gpiozero import MotionSensor,LED,Servo,Button
    import RPi.GPIO as GPIO
    import picamera
    import os

ABCD_HCSR04_IO=[(16,20),(9,11),(6,5),(13,19)]#(Trig,Echo)
ABCD_SERVO_IO=[14,15,18,23]
ABCD_LED_IO=[1,7,8,25]
ABCD_empty_dis=[100,100,100,100]
ABCD_full_dis=[40,40,40,40]
LightLED_IO=22
NetLED_IO=10
OpenBtn_IO=3
BRIGHT=70 #背光设置 0--100

Type2Num=[0,1,2,3,3]#垃圾类别->舵机编号的映射
OppSerNum=[2,3,0,1]#此舵机->对面舵机编号的映射
Type2Str=["recyclable","harmful","wet","dry","dry"]

ResetVal=[0.5,0.45,-0.15,0.5]
DownVal=[1,0.85,-0.6,1]
UpVal=[0.3,0.3,0,0.4]

Sers=[]
Leds=[]

def InitAll():
    if ENV.__ENV__ !="RaspberryPi":
        Sers.append("Ser0")
        Sers.append("Ser1")
        Sers.append("Ser2")
        Sers.append("Ser3")
        print("InitAll OK!")
        return
    global Light,NetLed,Btn
    Light=LED(LightLED_IO)
    NetLed=LED(NetLED_IO)
    Btn=Button(OpenBtn_IO)
    InitCam()
    InitSers()

def InitCam():
    global Camera
    Camera=picamera.PiCamera()
    Camera.brightness=BRIGHT

def InitSers():
    Sers=[]
    myCorrection=0.45
    maxPW=(2.0+myCorrection)/1000
    minPW=(1.0-myCorrection)/1000
    Ser0 = Servo(ABCD_SERVO_IO[0],min_pulse_width=minPW,max_pulse_width=maxPW)
    Ser1 = Servo(ABCD_SERVO_IO[1],min_pulse_width=minPW,max_pulse_width=maxPW)
    Ser2 = Servo(ABCD_SERVO_IO[2],min_pulse_width=minPW,max_pulse_width=maxPW)
    Ser3 = Servo(ABCD_SERVO_IO[3],min_pulse_width=minPW,max_pulse_width=maxPW)
    Ser0.detach()
    Ser1.detach()
    Ser2.detach()
    Ser3.detach()
    Sers.append(Ser0)
    Sers.append(Ser1)
    Sers.append(Ser2)
    Sers.append(Ser3)

def GetDis(Trig,Echo):
    if ENV.__ENV__ !="RaspberryPi":
        print("GetDis ("+str(Trig)+","+str(Echo)+"):50")
        return 50
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Trig,GPIO.OUT)
    GPIO.setup(Echo,GPIO.IN)
    #输出10us的方波脉冲
    GPIO.output(Trig,True)
    time.sleep(0.00001)
    GPIO.output(Trig,False)
    #等待ECHO的低电平结束
    while GPIO.input(Echo)==0:
        pass
    st=time.time()
    #等待高电平传回
    while GPIO.input(Echo)==1:
        pass
    ed=time.time()
    dis=(ed-st)*350*100/2
    GPIO.cleanup()
    return dis

def getNowINFO():
    if ENV.__ENV__ !="RaspberryPi":
        return "666"
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))


def capCam(_jpgfile):
    '''拍照保存到文件中，拍照过程中打开拍照指示灯和补光灯
    :param _jpgfile: 图片保存目录
    '''
    if ENV.__ENV__ !="RaspberryPi":
        print("Take a photo OK!")
        return
    Light.on()
    Camera.capture(_jpgfile)
    time.sleep(1)
    Light.off()

def STurn(ser,num):
    '''ser舵机旋转num后暂停1秒然后断开控制
    :param ser: 对应舵机
    :param num: 旋转值 从-1~0~1 建议用ResetVal[编号] DownVal数组
    '''
    if ENV.__ENV__ !="RaspberryPi":
        print("STurn: "+str(ser)+" : "+str(num)+" OK!")
        return
    ser.value=float(num)
    time.sleep(1)
    ser.detach()

def ResetSers():
    '''四个舵机恢复初始值
    '''
    if ENV.__ENV__ !="RaspberryPi":
        print("ResetSers OK!")
        return
    for i in range(4):
        STurn(Sers[i],ResetVal[i])

def DownSers():
    if ENV.__ENV__ !="RaspberryPi":
        print("DownSers OK!")
        return
    for i in range(4):
        STurn(Sers[i],DownVal[i])
