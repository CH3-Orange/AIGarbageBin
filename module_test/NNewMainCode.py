from gpiozero import MotionSensor,LED,Servo,Button
import RPi.GPIO as GPIO
from PIL import Image
import matplotlib.pyplot as plt
import picamera
import time,base64,json,requests
import socket
import os
import sys
import struct

BTNIO=21 #开门按钮IO口
LEDIO=19 #拍照LED I0O口
LIGHTIO=22 #补光灯IO口
NETLEDIO=10 #服务器通讯指示灯IO口
SERIOS=[14,15,17,23]
TIMEOUT=0.5 #扫描时间间隔
CHATTIMEOUT=9 #与服务器通讯间隔 实际暂停时间为CHATTIMEOUT*TIMEOUT秒
TIMESTOP=5
BRIGHT=60 #背光设置 0--100
jpgFile='image.jpg'
#0可回收，1有害，2厨余湿垃圾，3其他干垃圾
Type2Num=[0,1,2,3,3]#垃圾类别->舵机编号的映射
OppSerNum=[1,0,3,2]#此舵机->对面舵机编号的映射
Type2Str=["recyclable","harmful","wet","dry","dry"]
ResetVal=[0.4,-0.15,0.5,0.5]
DownVal=[1,-0.7,1,0.9]
UpVal=[0.3,0,0.3,0.4]
LEDSIO=[1,7,8,25]
Sers=[]
Leds=[]

Status="00"
Message=""

CamLed=LED(LEDIO)
Light=LED(LIGHTIO)
NetLed=LED(NETLEDIO)

Camera=picamera.PiCamera()
Camera.brightness=BRIGHT
Btn=Button(BTNIO)

    
def getNowINFO():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

def socket_client(STATUS,MESSAGE = ''):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '8.129.109.115'
        port = 9999
        s.connect((host, port))
    except socket.error as msg:
        print(msg)
        return
    if STATUS == '00':
        s.sendall(STATUS.encode('utf-8'))
        answer = s.recv(1024).decode('utf-8')
        if answer == 'GOTCHA':
            s.sendall('OK'.encode('utf-8'))
            answer =s.recv(1024).decode('utf-8')
            print(answer)
            if answer =='ShowMePhoto':
                DownSers()
                capCam(jpgFile)
                STATUS="01"
            elif answer =='Nothing':
                print(getNowINFO())
                s.sendall(getNowINFO().encode('utf-8'))
                s.close()
    if STATUS == '01':
        #s.sendall(STATUS.encode('utf-8'))
        #answer = s.recv(1024).decode('utf-8')
        if True:
            print(answer)
            while 1:
                filepath = jpgFile
                if os.path.isfile(filepath):
                    # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
                    fileinfo_size = struct.calcsize('128sl')
                    # 定义文件头信息，包含文件名和文件大小
                    fhead = struct.pack('128sl', bytes(os.path.basename(filepath).encode('utf-8')),os.stat(filepath).st_size)
                    s.send(fhead)
                    print ('client filepath: {0}'.format(filepath))
                    fp = open(filepath, 'rb')
                    while 1:
                        data = fp.read(1024)
                        if not data:
                            print ('{0} file send over...'.format(filepath))
                            break
                        s.send(data)
                s.close()
                ResetSers()
                Status="00"
                break
    if STATUS == '02':
        s.sendall(STATUS.encode('utf-8'))
        answer = s.recv(1024).decode('utf-8')
        if answer == 'GOTCHA':
            s.sendall(MESSAGE.encode('utf-8'))
            #MESSAGE格式：种类(recyclable,dry,wet,harmful)例：recyclable
            
        s.close()
        Status="00"

def capCam(_jpgfile):
    '''拍照保存到文件中，拍照过程中打开拍照指示灯和补光灯
    :param _jpgfile: 图片保存目录
    '''
    Light.on()
    CamLed.on()#指示灯 开
    Camera.capture(_jpgfile)
    time.sleep(1)
    CamLed.off()#指示灯 关
    Light.off()

def STurn(ser,num):
    '''ser舵机旋转num后暂停1秒然后断开控制
    :param ser: 对应舵机
    :param num: 旋转值 从-1~0~1 建议用ResetVal[编号] DownVal数组
    '''
    ser.value=float(num)
    time.sleep(1)
    ser.detach()

def ResetSers():
    for i in range(4):
        STurn(Sers[i],ResetVal[i])

def DownSers():
    for i in range(4):
        STurn(Sers[i],DownVal[i])
    
def identify(_jpgfile):
    jpg = open(_jpgfile, "rb")
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
    #print(ls)
    return ls

def main():
    cnt=0
    cnt2=0
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
    Sers.append(Ser0)
    Sers.append(Ser1)
    Sers.append(Ser2)
    Sers.append(Ser3)
    Leds.append(LED(LEDSIO[0]))
    Leds.append(LED(LEDSIO[1]))
    Leds.append(LED(LEDSIO[2]))
    Leds.append(LED(LEDSIO[3]))
    for i in range(4):
        Leds[i].on()
    time.sleep(3)
    for i in range(4):
        Leds[i].off()
    
    ResetSers()
    time.sleep(2)
    ResetSers()#再次恢复，避免第一次因为电压不稳导致个别舵机没有归位 
    #STurn(Sers[3],DownVal[3])
    while True:
        if(Btn.is_pressed):
            time.sleep(2)
            print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"YES")
            capCam(jpgFile)
            lajilist=identify(jpgFile)
            _lajiType=lajilist[0][1][1]
            lajistr=lajilist[0][0]
            if("瓶"in lajilist[0][0]):
                _lajiType=0
            if("盒"in lajilist[0][0]):
                _lajiType=0
            if("室内"in lajilist[0][0]):
                lajistr="包装盒"
                _lajiType=0
            if("扇"in lajilist[0][0]):
                lajistr="包装盒"
                _lajiType=0
            SerNum=Type2Num[_lajiType]#对应舵机的编号
            Leds[SerNum].on()
            print(lajistr+","+Type2Str[_lajiType])
            STurn(Sers[SerNum],DownVal[SerNum])
            time.sleep(1)
            STurn(Sers[OppSerNum[SerNum]],UpVal[OppSerNum[SerNum]])
            time.sleep(1.5)
            STurn(Sers[OppSerNum[SerNum]],ResetVal[OppSerNum[SerNum]])
            time.sleep(1)
            STurn(Sers[SerNum],ResetVal[SerNum])
            time.sleep(1)
            Leds[SerNum].off()
            ResetSers()

            Light.off() #关闭背光
            socket_client("02",lajistr+","+Type2Str[_lajiType])
        else:
            print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"no")
        cnt=cnt+1
        cnt2=cnt2+1
        if(cnt==CHATTIMEOUT):#与服务器通信
            cnt=0
            socket_client(Status)
        if(cnt2==20):
            cnt2=0
            ResetSers()


        time.sleep(TIMEOUT)
        

if __name__=="__main__":
    main()