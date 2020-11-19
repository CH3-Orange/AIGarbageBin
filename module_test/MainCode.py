from gpiozero import MotionSensor,LED,Servo,Button
import RPi.GPIO as GPIO
from PIL import Image
import matplotlib.pyplot as plt
import picamera
import time,base64,json,requests


def SelfCheck():
    pass

def identify(jpgfile):
    jpg = open(jpgfile, "rb")
    mykey="9f24a5e1f94efda4a631bf1da207b002"
    jpg64 =  base64.b64encode(jpg.read())
    jpg.close()
    url = 'http://api.tianapi.com/txapi/imglajifenlei/'
    body = {
        "key": mykey,
        "img": jpg64.decode(),
    }
    # print(body)
    headers = {'content-type': "application/x-www-form-urlencoded"}
    response = requests.post(url,headers=headers, data=body )
    if(response.status_code!=200):#出错
        return -1
    resJson=response.json()
    res={}
    if(resJson.get("newslist")):
        lajilist=resJson["newslist"]
        for item in lajilist:
            res[item.get("name")]=(item.get("trust"),item.get("lajitype"))

    # print(res)
    ls=list(res.items())
    ls=sorted(ls,key= lambda x:x[1][0],reverse=True)
    print(ls)
    return ls

if __name__=="__main__":

    BTNIO=21#开门按钮IO口
    LEDIO=19 #LED I0O口
    SERIOS=[14,15,17,18]
    TIMEOUT=1 #扫描时间间隔
    TIMESTOP=5
    BRIGHT=70 #背光设置 0--100
    jpgFile='image.jpg'

    myCorrection=0.45
    maxPW=(2.0+myCorrection)/1000
    minPW=(1.0-myCorrection)/1000
    Ser0 = Servo(SERIOS[0],min_pulse_width=minPW,max_pulse_width=maxPW)
    Ser1 = Servo(SERIOS[1],min_pulse_width=minPW,max_pulse_width=maxPW)
    Ser2 = Servo(SERIOS[2],min_pulse_width=minPW,max_pulse_width=maxPW)
    Ser3 = Servo(SERIOS[3],min_pulse_width=minPW,max_pulse_width=maxPW)
    
    Ser0.detach()
    Ser1.detach()
    Ser2.detach()
    Ser3.detach()
    
    
    led=LED(LEDIO)
    camera=picamera.PiCamera()
    camera.brightness=BRIGHT
    
    btn=Button(BTNIO)
    SelfCheck()
    time.sleep(TIMESTOP)
    FirstFlag=True
    while True:
        if(btn.is_pressed):    
            print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"YES")
            led.on()
            camera.capture(jpgFile)
            lajilist=identify(jpgFile)

            if(lajilist[0][1][1]==0):
                print(str(lajilist[0])+" 可回收")
                Ser0.max()
                time.sleep(5)
                Ser0.min()

            elif(lajilist[0][1][1]==1):
                print(str(lajilist[0])+" 有害垃圾")
                Ser1.max()
                time.sleep(5)
                Ser1.min()

            elif(lajilist[0][1][1]==2):
                print(str(lajilist[0])+" 厨余垃圾湿垃圾")
                Ser2.max()
                time.sleep(5)
                Ser2.min()
                
            else:#elif(eval(lajilist[0][1][1])==3):
                print(str(lajilist[0])+" 干垃圾其他垃圾")
                Ser3.max()
                time.sleep(5)
                Ser3.min()
            time.sleep(TIMESTOP)
            led.off()
        else:
            print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"no")
            led.off()
        Ser0.detach()
        Ser1.detach()
        Ser2.detach()
        Ser3.detach()
        time.sleep(TIMEOUT)
