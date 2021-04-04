import ENV
from PySide2.QtWidgets import QApplication, QMessageBox,QLabel
from PySide2.QtUiTools import QUiLoader
from threading import Thread
from PySide2.QtGui import QPixmap
from PySide2.QtCore import QFile,QThread,Signal,QObject
from PIL import Image
import matplotlib.pyplot as plt
import time,base64,json,requests
import socket,os,sys,struct,time

import raspberryPi as rasp
import Identify


########全局变量########
ABCD_clear_dis=[]#四个桶的空载距离
# ABCD_HCSR04_IO=[(16,20),(9,11),(6,5),(13,19)]#(Trig,Echo)
# ABCD_SERVO_IO=[14,15,18,23]
# ABCD_LED_IO=[1,7,8,25]
# LightLED_IO=22
# NetLED_IO=10
# OpenBtn_IO=3
ABCD_ENname=["green","red","blue","yellow"]
ABCD_CHname=["可回收","有害垃圾","厨余垃圾","其他垃圾"]
TIMEOUT=1 #扫描时间间隔
CHATTIMEOUT=5 #与服务器通讯间隔 实际暂停时间为CHATTIMEOUT*TIMEOUT秒
TIMESTOP=5
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
# Light=LED(LightLED_IO)
# NetLed=LED(NetLED_IO)
# Camera=picamera.PiCamera()
# Camera.brightness=BRIGHT
# Btn=Button(OpenBtn_IO)
########全局变量########

class mySignals(QObject):
    update_pic_signal=Signal(int,int)
    update_his_signal=Signal(str)
    update_info_signal=Signal(str)
    update_lajipic_signal=Signal(str)
    update_net_signal=Signal(str)
# global_ms=mySignals()


class Form:

    def __init__(self):
        
        self.ui = QUiLoader().load(uiPath)
        self.ms=mySignals()
        self.ms.update_pic_signal.connect(self.update_pic_slot)
        self.ms.update_his_signal.connect(self.update_his_slot)
        self.ms.update_info_signal.connect(self.update_info_slot)
        self.ms.update_lajipic_signal.connect(self.update_lajipic_slot)
        self.ms.update_net_signal.connect(self.update_net_slot)
        self.PicList=[self.ui.greenPic,self.ui.bluePic,self.ui.redPic,self.ui.yellowPic]
        self.LabelList=[self.ui.greenLabel,self.ui.blueLabel,self.ui.redLabel,self.ui.yellowLabel]
        # self.setBtn.clicked.connect(setBtn_click)
        #self.ui.Button.clicked.connect(self.ButtonClick)
        # global_ms.update_pic_signal.connect(update_pic_slot)
    def update_net_slot(self,str):
        self.ui.NetLabel.setText(str)
    def update_net(self,str):
        self.ms.update_net_signal.emit(str)
    def update_lajipic_slot(self,jpgpath):
        # print("+++"+jpgpath)
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
    def update_his(self,str):
        self.ms.update_his_signal.emit(str)
    
    def update_pic_slot(self,num,nowdis):
        piclabel=self.PicList[num]
        label=self.LabelList[num]
        # percent=(1-nowdis/ABCD_clear_dis[num])*5
        percent=nowdis/100*5
        label.setText(ABCD_CHname[num]+":"+str(nowdis)[0:5]+"%")
        percent=round(percent)
        PicPath=PicBasePath+"/"
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
        print((num,nowdis))
        self.ms.update_pic_signal.emit(num,nowdis)

def BackThread():
    ######初始化#####
    ABCD_clear_dis.append(90);
    ABCD_clear_dis.append(90);
    ABCD_clear_dis.append(90);
    ABCD_clear_dis.append(90);
    ljcnt=[0,0,0,0]#不同种类垃圾的计数
    ljAllcnt=0
    cnt=0

    rasp.InitAll()

    rasp.ResetSers()
    time.sleep(2)
    rasp.ResetSers()#再次恢复，避免第一次因为电压不稳导致个别舵机没有归位 
    ######初始化#####
    
    form.update_dis(3,0)
    form.update_dis(0,0)
    form.update_dis(1,0)
    form.update_dis(2,0)
    form.update_lajipic(bannerPath)
    _cnt=0
    while True:
        
        temp=rasp.getNowINFO()
        form.update_info(temp)
        _cnt=_cnt+1
        # if(Btn.is_pressed):
        if(_cnt==5): 
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
            else:
                pass
            # rasp.Light.off() #关闭背光
            #socket_client("02",str(lajilist[0])+","+Type2Str[_lajiType])
        else:
            print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"no")
        cnt=cnt+1
        # if(cnt==CHATTIMEOUT):#与服务器通信
        #     cnt=0
        #     socket_client("00")


        time.sleep(TIMEOUT)

app = QApplication([])
form = Form()
form.ui.show()
back_thread=Thread(target=BackThread)
back_thread.start()
app.exec_()