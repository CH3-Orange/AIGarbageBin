<<<<<<< HEAD
from PySide2.QtWidgets import QApplication, QMessageBox,QLabel
=======
import ENV
from PySide2.QtWidgets import QApplication, QMessageBox,QLabel,QWidget
>>>>>>> f53759334b0ebe072dfc005f5a8217d32f6b5627
from PySide2.QtUiTools import QUiLoader
from threading import Thread
from PySide2.QtGui import QPixmap
from PySide2.QtCore import QFile,QThread,Signal,QObject
<<<<<<< HEAD
# from gpiozero import MotionSensor,LED,Servo,Button
# import RPi.GPIO as GPIO
from PIL import Image
import matplotlib.pyplot as plt
# import picamera
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
=======
from PIL import Image
import matplotlib.pyplot as plt
import time,base64,json,requests
import socket,os,sys,struct,time

import raspberryPi as rasp
import Identify
import windows2


########全局变量########
ABCD_clear_dis=[]#四个桶的空载距离
# ABCD_HCSR04_IO=[(16,20),(9,11),(6,5),(13,19)]#(Trig,Echo)
# ABCD_SERVO_IO=[14,15,18,23]
# ABCD_LED_IO=[1,7,8,25]
# LightLED_IO=22
# NetLED_IO=10
# OpenBtn_IO=3
>>>>>>> f53759334b0ebe072dfc005f5a8217d32f6b5627
ABCD_ENname=["green","red","blue","yellow"]
ABCD_CHname=["可回收","有害垃圾","厨余垃圾","其他垃圾"]
TIMEOUT=1 #扫描时间间隔
CHATTIMEOUT=5 #与服务器通讯间隔 实际暂停时间为CHATTIMEOUT*TIMEOUT秒
TIMESTOP=5
<<<<<<< HEAD
BRIGHT=70 #背光设置 0--100
jpgFile='image.jpg'
#0可回收，1有害，2厨余湿垃圾，3其他干垃圾
Type2Num=[0,1,2,3,3]#垃圾类别->舵机编号的映射
OppSerNum=[2,3,0,1]#此舵机->对面舵机编号的映射
Type2Str=["recyclable","harmful","wet","dry","dry"]
ResetVal=[0.5,0.45,-0.15,0.5]
DownVal=[1,0.85,-0.6,1]
UpVal=[0.3,0.3,0,0.4]
Sers=[]
Leds=[]
=======
# BRIGHT=70 #背光设置 0--100
if ENV.__ENV__=="RaspberryPi":
    jpgFile='image.png'
    bannerPath=r"/home/pi/Desktop/AIGarbageBin/From/jpg/banner0.png"
    PicBasePath=r'/home/pi/Desktop/AIGarbageBin/From/jpg'
    uiPath=r'/home/pi/Desktop/AIGarbageBin/From/ui/windows_ui.ui'
elif ENV.__ENV__=="Windows":
    jpgFile='From\image.png'
    bannerPath=r"D:\Program\Python\RaspberryPi\AIGarbageBin\From\jpg\banner0.png"
    PicBasePath=r'D:\Program\Python\RaspberryPi\AIGarbageBin\From\jpg'
    uiPath=r'D:\Program\Python\RaspberryPi\AIGarbageBin\From\ui\windows_ui.ui'



# #0可回收，1有害，2厨余湿垃圾，3其他干垃圾
# Type2Num=[0,1,2,3,3]#垃圾类别->舵机编号的映射
# OppSerNum=[2,3,0,1]#此舵机->对面舵机编号的映射
# ResetVal=[0.5,0.45,-0.15,0.5]
# DownVal=[1,0.85,-0.6,1]
# UpVal=[0.3,0.3,0,0.4]
# Sers=[]
# Leds=[]
>>>>>>> f53759334b0ebe072dfc005f5a8217d32f6b5627
# Light=LED(LightLED_IO)
# NetLed=LED(NetLED_IO)
# Camera=picamera.PiCamera()
# Camera.brightness=BRIGHT
# Btn=Button(OpenBtn_IO)
<<<<<<< HEAD
bannerPath=r"D:\Program\Python\RaspberryPi\From\jpg\banner0.jpg"

########全局变量########
def GetDis(Trig,Echo):
    pass
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

=======
########全局变量########
>>>>>>> f53759334b0ebe072dfc005f5a8217d32f6b5627

class mySignals(QObject):
    update_pic_signal=Signal(int,int)
    update_his_signal=Signal(str)
    update_info_signal=Signal(str)
    update_lajipic_signal=Signal(str)
    update_net_signal=Signal(str)
# global_ms=mySignals()


<<<<<<< HEAD
class Form:

    def __init__(self):
        
        self.ui = QUiLoader().load(r'D:\Program\Python\RaspberryPi\From\ui\windows_ui.ui')
=======
class Form(QWidget):

    def __init__(self):
        super(Form,self).__init__()
        self.ui = QUiLoader().load(uiPath)
>>>>>>> f53759334b0ebe072dfc005f5a8217d32f6b5627
        self.ms=mySignals()
        self.ms.update_pic_signal.connect(self.update_pic_slot)
        self.ms.update_his_signal.connect(self.update_his_slot)
        self.ms.update_info_signal.connect(self.update_info_slot)
        self.ms.update_lajipic_signal.connect(self.update_lajipic_slot)
        self.ms.update_net_signal.connect(self.update_net_slot)
        self.PicList=[self.ui.greenPic,self.ui.bluePic,self.ui.redPic,self.ui.yellowPic]
        self.LabelList=[self.ui.greenLabel,self.ui.blueLabel,self.ui.redLabel,self.ui.yellowLabel]
<<<<<<< HEAD
        # self.setBtn.clicked.connect(setBtn_click)
=======
        self.ui.setBtn.clicked.connect(self.setBtn_clicked)
>>>>>>> f53759334b0ebe072dfc005f5a8217d32f6b5627
        #self.ui.Button.clicked.connect(self.ButtonClick)
        # global_ms.update_pic_signal.connect(update_pic_slot)
    def update_net_slot(self,str):
        self.ui.NetLabel.setText(str)
    def update_net(self,str):
        self.ms.update_net_signal.emit(str)
    def update_lajipic_slot(self,jpgpath):
<<<<<<< HEAD
=======
        # print("+++"+jpgpath)
>>>>>>> f53759334b0ebe072dfc005f5a8217d32f6b5627
        pixmap=QPixmap(jpgpath)
        pixmap=pixmap.scaled(self.ui.moviePlayer.size())
        self.ui.moviePlayer.setPixmap(pixmap)
        self.ui.moviePlayer.setScaledContents(True)
        self.ui.moviePlayer.show()
    def update_lajipic(self,jpgpath):
        self.ms.update_lajipic_signal.emit(jpgpath)
    def update_info_slot(self,str):
        self.ui.infoLabel.setText("主板温度："+str+"℃\n"+"目前状态：正常")
    def update_info(self,str):
        self.ms.update_info_signal.emit(str)
    def update_his_slot(self,str):
        self.ui.hisList.appendPlainText(str)
<<<<<<< HEAD
    def update_his(self,str):
        self.ms.update_his_signal.emit(str)
    def setBtn_click(self):
        pass
    def update_pic_slot(self,num,nowdis):
        piclabel=self.PicList[num]
        label=self.LabelList[num]
        # percent=(1-nowdis/ABCD_clear_dis[num])*5
        percent=nowdis/100*5
        label.setText(ABCD_CHname[num]+":"+str(nowdis)[0:5]+"%")
        percent=round(percent)
        PicPath=r'D:\Program\Python\RaspberryPi\From\jpg\\'
=======
        self.ui.hisList.ensureCursorVisible()# 内容超出控件时会向下滚动
    def update_his(self,str):
        self.ms.update_his_signal.emit(str)
    
    def update_pic_slot(self,num,nowdis):
        piclabel=self.PicList[num]
        label=self.LabelList[num]
        # percent=nowdis/100*5
        percent=(nowdis-rasp.ABCD_full_dis[num])*5/(rasp.ABCD_empty_dis[num]-rasp.ABCD_full_dis[num])

        label.setText(ABCD_CHname[num]+":"+str(nowdis)[0:5]+"%")
        percent=round(percent)
        PicPath=PicBasePath+"/"
>>>>>>> f53759334b0ebe072dfc005f5a8217d32f6b5627
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
<<<<<<< HEAD
        # percent=int(nowdis/ABCD_clear_dis[num]*5)
        print((num,nowdis))
        self.ms.update_pic_signal.emit(num,nowdis)
app = QApplication([])
form = Form()
   
def getNowINFO():
    return "90"
    # pass
    # res = os.popen('vcgencmd measure_temp').readline()
    # return(res.replace("temp=","").replace("'C\n",""))

def socket_client(STATUS,MESSAGE = ''):
    try:
        form.update_net("Net:Connecting...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '8.129.109.115'
        port = 9999
        s.connect((host, port))
    except socket.error as msg:
        print(msg)
        form.update_net("Net:"+msg)
        sys.exit(1)
    if STATUS == '00':
        s.sendall(STATUS.encode('utf-8'))
        answer = s.recv(1024).decode('utf-8')
        if answer == 'GOTCHA':
            s.sendall('OK'.encode('utf-8'))
            answer == s.recv(1024).decode('utf-8')
            form.update_net("Net:"+answer)
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
    pass
    Light.on()
    Camera.capture(_jpgfile)
    time.sleep(1)
    Light.off()

def STurn(ser,num):
    '''ser舵机旋转num后暂停1秒然后断开控制
    :param ser: 对应舵机
    :param num: 旋转值 从-1~0~1 建议用ResetVal[编号] DownVal数组
    '''
    pass
    ser.value=float(num)
    time.sleep(1)
    ser.detach()

def ResetSers():
    '''四个舵机恢复初始值
    '''
    pass
    for i in range(4):
        STurn(Sers[i],ResetVal[i])

def DownSers():
    pass
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
=======
        print((num,nowdis))
        self.ms.update_pic_signal.emit(num,nowdis)
    def setBtn_clicked(self):
        # MessageBox=QMessageBox()
        # MessageBox.information(self.ui,"这是一个标题","这里有内容")
        
        ENV.blockFlag=1#设置后台的进程为阻塞状态
        self.form2 = windows2.Form2()
        self.form2.ui.show()
        # self.form2.exec_()
>>>>>>> f53759334b0ebe072dfc005f5a8217d32f6b5627

def BackThread():
    ######初始化#####
    ABCD_clear_dis.append(90);
    ABCD_clear_dis.append(90);
    ABCD_clear_dis.append(90);
    ABCD_clear_dis.append(90);
<<<<<<< HEAD
    cnt=0
    myCorrection=0.45
    maxPW=(2.0+myCorrection)/1000
    minPW=(1.0-myCorrection)/1000
    # Ser0 = Servo(ABCD_SERVO_IO[0],min_pulse_width=minPW,max_pulse_width=maxPW)
    # Ser1 = Servo(ABCD_SERVO_IO[1],min_pulse_width=minPW,max_pulse_width=maxPW)
    # Ser2 = Servo(ABCD_SERVO_IO[2],min_pulse_width=minPW,max_pulse_width=maxPW)
    # Ser3 = Servo(ABCD_SERVO_IO[3],min_pulse_width=minPW,max_pulse_width=maxPW)
    # Ser0.detach()
    # Ser1.detach()
    # Ser2.detach()
    # Ser3.detach()
    # Sers.append(Ser0)
    # Sers.append(Ser1)
    # Sers.append(Ser2)
    # Sers.append(Ser3)
    

    # ResetSers()
    time.sleep(2)
    # ResetSers()#再次恢复，避免第一次因为电压不稳导致个别舵机没有归位 
    ######初始化#####
    
    form.update_dis(3,0)
    form.update_dis(0,0)
    form.update_dis(1,0)
    form.update_dis(2,0)
    form.update_lajipic(bannerPath)
    _cnt=0
    while True:
        #if(Btn.is_pressed):
        temp=getNowINFO()
        form.update_info(temp)
        _cnt=_cnt+1
        if(_cnt==5): 
            _cnt=0 
            print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"YES")
            # capCam(jpgFile)
            lajilist=identify(jpgFile)
            print(lajilist)
            _lajiType=lajilist[0][1][1]
            SerNum=Type2Num[_lajiType]#对应舵机的编号
            #Leds[SerNum].on()
            print(str(lajilist[0])+","+Type2Str[_lajiType])
            form.update_his(str(lajilist[0])+","+Type2Str[_lajiType])
            def change_lajipic_thread():
                # form.update_lajipic(jpgFile)
                form.update_lajipic(r"D:\Program\Python\RaspberryPi\From\image.jpg")
                time.sleep(3)
                form.update_lajipic(bannerPath)#恢复展示宣传图
            ChangeLajipicThread=Thread(target=change_lajipic_thread)
            ChangeLajipicThread.start()
            # STurn(Sers[SerNum],DownVal[SerNum])
            time.sleep(1)
            # STurn(Sers[OppSerNum[SerNum]],UpVal[OppSerNum[SerNum]])
            time.sleep(1.5)
            # STurn(Sers[OppSerNum[SerNum]],ResetVal[OppSerNum[SerNum]])
            time.sleep(1)
            # STurn(Sers[SerNum],ResetVal[SerNum])
            time.sleep(1)
            #Leds[SerNum].off()
            # ResetSers()

            # Light.off() #关闭背光
=======
    ljcnt=[0,0,0,0]#不同种类垃圾的计数
    ljAllcnt=0
    cnt=0

    rasp.InitAll()

    rasp.ResetSers()
    time.sleep(2)
    rasp.ResetSers()#再次恢复，避免第一次因为电压不稳导致个别舵机没有归位 
    ######初始化#####
    
    form.update_dis(0,100)
    form.update_dis(1,80)
    form.update_dis(2,60)
    form.update_dis(3,50)
    form.update_lajipic(bannerPath)
    _cnt=0
    while True:
        if ENV.ExitFlag==1: #进程结束信号
            break
        while ENV.blockFlag==1:
            print("后台进程阻塞中...")
            time.sleep(2)
            pass
        temp=rasp.getNowINFO()
        form.update_info(temp)
        _cnt=_cnt+1
        # if(Btn.is_pressed):
        if(_cnt==10): 
            _cnt=0 
            print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"YES")
            if ENV.__ENV__=="RaspberryPi":
                rasp.capCam(jpgFile)
            # lajilist=identify(jpgFile)
            # print(lajilist)
            # _lajiType=lajilist[0][1][1]
            lajilist=Identify.BDTXidentify(jpgFile)#垃圾分类查询返回 ('名称', 代号, '类别')
            print(lajilist)
            if lajilist !=-1:
                ljcnt[lajilist[1]]+=1 #对应垃圾类别数量+1
                ljAllcnt+=1 #垃圾总数+1
                SerNum=rasp.Type2Num[lajilist[1]]#对应舵机的编号
                #Leds[SerNum].on()
                # print(str(ljAllcnt)+str(lajilist[0])+","+str(lajilist[0]))
                print("{0} {1} {3} {2} OK!".format(str(ljAllcnt),lajilist[0],ljcnt[lajilist[1]],rasp.Type2Str[lajilist[1]]))
                form.update_his("{0} {1} {3} {2} OK!".format(str(ljAllcnt),lajilist[0],ljcnt[lajilist[1]],rasp.Type2Str[lajilist[1]]))
                def change_lajipic_thread():
                    if ENV.__ENV__=="RaspberryPi":
                        form.update_lajipic(jpgFile)
                    if ENV.__ENV__=="Windows":
                        # form.update_lajipic(r"D:\Program\Python\RaspberryPi\AIGarbageBin\From\image.png")
                        form.update_lajipic(jpgFile)
                    time.sleep(3)
                    form.update_lajipic(bannerPath)#恢复展示宣传图
                ChangeLajipicThread=Thread(target=change_lajipic_thread)
                ChangeLajipicThread.start()
                rasp.STurn(rasp.Sers[SerNum],rasp.DownVal[SerNum])
                time.sleep(1)
                rasp.STurn(rasp.Sers[rasp.OppSerNum[SerNum]],rasp.UpVal[rasp.OppSerNum[SerNum]])
                time.sleep(1.5)
                rasp.STurn(rasp.Sers[rasp.OppSerNum[SerNum]],rasp.ResetVal[rasp.OppSerNum[SerNum]])
                time.sleep(1)
                rasp.STurn(rasp.Sers[SerNum],rasp.ResetVal[SerNum])
                time.sleep(1)
                # Leds[SerNum].off()
                rasp.ResetSers()
                dis=rasp.GetDis(rasp.ABCD_HCSR04_IO[SerNum][0],rasp.ABCD_HCSR04_IO[SerNum][1])
                form.update_dis(SerNum,dis)
                #这里要满载判断
            else:
                pass
            # rasp.Light.off() #关闭背光
>>>>>>> f53759334b0ebe072dfc005f5a8217d32f6b5627
            #socket_client("02",str(lajilist[0])+","+Type2Str[_lajiType])
        else:
            print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"no")
        cnt=cnt+1
        # if(cnt==CHATTIMEOUT):#与服务器通信
        #     cnt=0
        #     socket_client("00")


        time.sleep(TIMEOUT)

<<<<<<< HEAD



=======
app = QApplication([])
form = Form()
>>>>>>> f53759334b0ebe072dfc005f5a8217d32f6b5627
form.ui.show()
back_thread=Thread(target=BackThread)
back_thread.start()
app.exec_()
<<<<<<< HEAD
=======
ENV.ExitFlag=1
>>>>>>> f53759334b0ebe072dfc005f5a8217d32f6b5627
