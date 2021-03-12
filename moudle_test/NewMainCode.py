from gpiozero import MotionSensor,LED,Servo,Button
import RPi.GPIO as GPIO
from PIL import Image
import matplotlib.pyplot as plt
import picamera
import time,base64,json,requests


def SelfCheck():
    pass
def ChatWithServer():
    pass

def STurn(ser,num):
    ser.value=float(num)
    time.sleep(1)
    ser.detach()
    
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
    LIGHTIO=22#补光灯IO口
    SERIOS=[14,15,17,18]
    TIMEOUT=1 #扫描时间间隔
    TIMESTOP=5
    BRIGHT=70 #背光设置 0--100
    jpgFile='image.jpg'
    #0可回收，1有害，2厨余湿垃圾，3其他干垃圾
    Type2Num=[0,1,2,3,3]#垃圾类别->舵机编号的映射
    OppSerNum=[1,0,3,2]#此舵机->对面舵机编号的映射
    Type2Str=["可回收","有害","厨余湿垃圾","其他","干垃圾"]
    myCorrection=0.45
    maxPW=(2.0+myCorrection)/1000
    minPW=(1.0-myCorrection)/1000
    ResetVal=[0.4,-0.15,0.5,0.55]
    DownVal=[1,-0.7,1,1]
    UpVal=[0.3,0,0.3,0.4]
    Ser0 = Servo(SERIOS[0],min_pulse_width=minPW,max_pulse_width=maxPW)
    Ser1 = Servo(SERIOS[1],min_pulse_width=minPW,max_pulse_width=maxPW)
    Ser2 = Servo(SERIOS[2],min_pulse_width=minPW,max_pulse_width=maxPW)
    Ser3 = Servo(SERIOS[3],min_pulse_width=minPW,max_pulse_width=maxPW)
    Sers=[Ser0,Ser1,Ser2,Ser3]
    Ser0.detach()
    Ser1.detach()
    Ser2.detach()
    Ser3.detach()
    
    
    Led=LED(LEDIO)
    Light=LED(LIGHTIO)
    Camera=picamera.PiCamera()
    Camera.brightness=BRIGHT
    
    Btn=Button(BTNIO)

    #time.sleep(TIMESTOP)
    for i in range(4):
        STurn(Sers[i],ResetVal[i])
    time.sleep(2)
    for i in range(4):
        STurn(Sers[i],ResetVal[i])   

    while True:
        if(Btn.is_pressed):    
            print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"YES")
            Light.on()
            Led.on()#指示灯 开
            Camera.capture(jpgFile)
            lajilist=identify(jpgFile)
            time.sleep(1)
            Led.off()#指示灯 关

            _lajiType=lajilist[0][1][1]
            SerNum=Type2Num[_lajiType]#对应舵机的编号
            print(str(lajilist[0])+Type2Str[_lajiType])
            STurn(Sers[SerNum],DownVal[SerNum])
            time.sleep(1)
            STurn(Sers[OppSerNum[SerNum]],UpVal[OppSerNum[SerNum]])
            time.sleep(1.5)
            STurn(Sers[OppSerNum[SerNum]],ResetVal[OppSerNum[SerNum]])
            time.sleep(1)
            STurn(Sers[SerNum],ResetVal[SerNum])
            time.sleep(1)
            for i in range(4):
                STurn(Sers[i],ResetVal[i]) 

            # if(lajilist[0][1][1]==0):
            #     print(str(lajilist[0])+" 可回收")
            #     Ser0.max()
            #     time.sleep(5)
            #     Ser0.min()

            # elif(lajilist[0][1][1]==1):
            #     print(str(lajilist[0])+" 有害垃圾")
            #     Ser1.max()
            #     time.sleep(5)
            #     Ser1.min()

            # elif(lajilist[0][1][1]==2):
            #     print(str(lajilist[0])+" 厨余垃圾湿垃圾")
            #     Ser2.max()
            #     time.sleep(5)
            #     Ser2.min()
                
            # else:#elif(eval(lajilist[0][1][1])==3):
            #     print(str(lajilist[0])+" 干垃圾其他垃圾")
            #     Ser3.max()
            #     time.sleep(5)
            #     Ser3.min()
            # time.sleep(TIMESTOP)
            Light.off()
        else:
            print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"no")
            Led.off()
        time.sleep(TIMEOUT)
        ChatWithServer()
