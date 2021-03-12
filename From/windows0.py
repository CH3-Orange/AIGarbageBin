from PySide2.QtWidgets import QApplication, QMessageBox,QLabel
from PySide2.QtUiTools import QUiLoader
from threading import Thread
from PySide2.QtGui import QPixmap
from PySide2.QtCore import QFile,QThread,Signal,QObject
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
import time
########全局变量########
ABCD_clear_dis=[]#四个桶的空载距离
ABCD_HCSR04_IO=[(16,20),(9,11),(6,5),(13,19)]#(Trig,Echo)
ABCD_SERVO_IO=[14,15,18,23]
ABCD_LED_IO=[1,7,8,25]
LightLED_IO=22
NetLED_IO=10
OpenBtn_IO=3
ABCD_ENname=["green","red","blue","yellow"]
ABCD_CHname=["可回收","有害垃圾","厨余垃圾","其他垃圾"]
TIMEOUT=1 #扫描时间间隔
CHATTIMEOUT=5 #与服务器通讯间隔 实际暂停时间为CHATTIMEOUT*TIMEOUT秒
TIMESTOP=5
BRIGHT=70 #背光设置 0--100
jpgFile='image.jpg'
Type2Num=[0,1,2,3,3]#垃圾类别->舵机编号的映射
OppSerNum=[2,3,0,1]#此舵机->对面舵机编号的映射
Type2Str=["recyclable","harmful","wet","dry","dry"]
ResetVal=[-0.5,0.4,-0.5,0.3]
DownVal=[-1,1,-1,1]
UpVal=[-0.6,0.5,-0.6,0.4]
Sers=[]
Leds=[]
Light=LED(LightLED_IO)
NetLed=LED(NetLED_IO)

Camera=picamera.PiCamera()
Camera.brightness=BRIGHT
Btn=Button(OpenBtn_IO)

########全局变量########
def GetDis(Trig,Echo):
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


class mySignals(QObject):
    update_pic_signal=Signal(int,int)
# global_ms=mySignals()


class Form:

    def __init__(self):
        
        self.ui = QUiLoader().load(r'/home/pi/Desktop/From/ui/windows_ui.ui')
        self.ms=mySignals()
        self.ms.update_pic_signal.connect(self.update_pic_slot)
        self.PicList=[self.ui.greenPic,self.ui.bluePic,self.ui.redPic,self.ui.yellowPic]
        self.LabelList=[self.ui.greenLabel,self.ui.blueLabel,self.ui.redLabel,self.ui.yellowLabel]
        #self.setBtn.clicked.connect(setBtn_click)
        #self.ui.Button.clicked.connect(self.ButtonClick)
        # global_ms.update_pic_signal.connect(update_pic_slot)
    def setBtn_click(self):
        pass
    def update_pic_slot(self,num,nowdis):
        piclabel=self.PicList[num]
        label=self.LabelList[num]
        percent=(1-nowdis/ABCD_clear_dis[num])*5
        label.setText(ABCD_CHname[num]+":"+str(percent))
        percent=int(percent)
        PicPath=r'/home/pi/Desktop/From/jpg/'
        if(percent<=5 and percent>=0 ):
            PicPath+=ABCD_ENname[num]+str(percent)+".png"
        else:
            PicPath+="Error.png"
        pixmap=QPixmap(PicPath)
        pixmap=pixmap.scaled(piclabel.size())
        piclabel.setPixmap(pixmap)
        piclabel.setScaledContents(True)
        piclabel.show()
        # label.setText(str(now_num))
    def update_dis(self,num,nowdis):#垃圾桶编号和当前距离
        # percent=int(nowdis/ABCD_clear_dis[num]*5)
        self.ms.update_pic_signal.emit(num,nowdis)
app = QApplication([])
form = Form()
   
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
        sys.exit(1)
    if STATUS == '00':
        s.sendall(STATUS.encode('utf-8'))
        answer = s.recv(1024).decode('utf-8')
        if answer == 'GOTCHA':
            s.sendall('OK'.encode('utf-8'))
            answer == s.recv(1024).decode('utf-8')
            if answer =='ShowMePhoto':
                capCam(jpgFile)
                STATUS="01"
            elif answer =='Nothing':
                s.sendall(getNowINFO().encode('utf-8'))
        s.close()
    if STATUS == '01':
        s.sendall(STATUS.encode('utf-8'))
        answer = s.recv(1024).decode('utf-8')
        if answer == 'GOTCHA':
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
                break
    elif STATUS == '02':
        s.sendall(STATUS.encode('utf-8'))
        answer = s.recv(1024).decode('utf-8')
        if answer == 'GOTCHA':
            s.sendall(MESSAGE.encode('utf-8'))
            #MESSAGE格式：种类(recyclable,dry,wet,harmful)例：recyclable
        s.close()

def capCam(_jpgfile):
    '''拍照保存到文件中，拍照过程中打开拍照指示灯和补光灯
    :param _jpgfile: 图片保存目录
    '''
    Light.on()
    Camera.capture(_jpgfile)
    time.sleep(1)
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
    '''四个舵机恢复初始值
    '''
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

def BackThread():
    ######初始化#####
    ABCD_clear_dis.append(90);
    ABCD_clear_dis.append(90);
    ABCD_clear_dis.append(90);
    ABCD_clear_dis.append(90);
    cnt=0
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
    

    ResetSers()
    time.sleep(2)
    ResetSers()#再次恢复，避免第一次因为电压不稳导致个别舵机没有归位 
    ######初始化#####
    
    form.update_dis(3,20)
    form.update_dis(0,2)
    form.update_dis(1,10)
    form.update_dis(2,6)
    while True:
        if(Btn.is_pressed):    
            print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"YES")
            capCam(jpgFile)
            lajilist=identify(jpgFile)
            _lajiType=lajilist[0][1][1]
            
            SerNum=Type2Num[_lajiType]#对应舵机的编号
            #Leds[SerNum].on()
            print(str(lajilist[0])+","+Type2Str[_lajiType]+","+str(SerNum))
            STurn(Sers[SerNum],DownVal[SerNum])
            time.sleep(1)
            STurn(Sers[OppSerNum[SerNum]],UpVal[OppSerNum[SerNum]])
            time.sleep(1.5)
            STurn(Sers[OppSerNum[SerNum]],ResetVal[OppSerNum[SerNum]])
            time.sleep(1)
            STurn(Sers[SerNum],ResetVal[SerNum])
            time.sleep(1)
            #Leds[SerNum].off()
            ResetSers()

            Light.off() #关闭背光
            #socket_client("02",str(lajilist[0])+","+Type2Str[_lajiType])
        else:
            print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"no")
        cnt=cnt+1
        if(cnt==CHATTIMEOUT):#与服务器通信
            cnt=0
            #socket_client("00")


        time.sleep(TIMEOUT)




form.ui.show()
back_thread=Thread(target=BackThread)
back_thread.start()
app.exec_()

