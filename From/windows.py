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
import jieba
import time
########全局变量########
# ABCD_clear_dis=[43,39,41,38]#四个桶的空载距离
ABCD_clear_dis=[]
ABCD_full_dis=[10,10,10,10]
ABCD_HCSR04_IO=[(16,20),(9,11),(6,5),(13,19)]#(Trig,Echo)
ABCD_SERVO_IO=[14,15,18,23]
ABCD_LED_IO=[1,7,8,25]
LightLED_IO=22
NetLED_IO=10
OpenBtn_IO=3
ABCD_ENname=["green","red","blue","yellow"]
ABCD_CHname=["可回收","有害垃圾","厨余垃圾","干垃圾"]
TIMEOUT=1 #扫描时间间隔
CHATTIMEOUT=5 #与服务器通讯间隔 实际暂停时间为CHATTIMEOUT*TIMEOUT秒
TIMESTOP=5
BRIGHT=65 #背光设置 0--100
jpgFile='image.jpg'
#0可回收，1有害，2厨余湿垃圾，3其他干垃圾
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
bannerPath=r"/home/pi/Desktop/From/jpg/banner0.jpg"

cntlaji=0
CheatLaji=["瓶子","纸巾","包装盒","电池","梨"]
CheatLajiType=["recyclable","dry","recyclable","harmful","wet"]


########全局变量########
def GetDis(Trig,Echo):
    pass
    
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
   
    return dis


class mySignals(QObject):
    update_pic_signal=Signal(int,int)
    update_his_signal=Signal(str)
    update_info_signal=Signal(str)
    update_lajipic_signal=Signal(str)
    update_net_signal=Signal(str)
# global_ms=mySignals()


class Form:

    def __init__(self):
        
        self.ui = QUiLoader().load(r'/home/pi/Desktop/From/ui/windows_ui.ui')
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
        self.ui.QRPic.setText(str)
    def update_net(self,str):
        self.ms.update_net_signal.emit(str)
    def update_lajipic_slot(self,jpgpath):
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
    def setBtn_click(self):
        pass
    def update_pic_slot(self,num,nowdis):
        piclabel=self.PicList[num]
        label=self.LabelList[num]
        # percent=(1-nowdis/ABCD_clear_dis[num])*5
        percent=((ABCD_clear_dis[num]-nowdis)/(ABCD_clear_dis[num]-ABCD_full_dis[num]))*5
        
        label.setText(ABCD_CHname[num]+":"+str(percent*20)[0:4]+"%")
        percent=round(percent)
        PicPath=r'/home/pi/Desktop/From/jpg/'
        if(percent<=5 and percent>=0 ):
            PicPath+=ABCD_ENname[num]+str(percent)+".png"
#             print(PicPath)
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
app = QApplication([])
form = Form()
   
def getNowINFO():
    #return "90"
    # pass
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

def socket_client(STATUS,MESSAGE = ''):
    try:
        form.update_net("Net:Connecting...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '8.129.109.115'
        port = 9999
        s.connect((host, port))
    except socket.error as msg:
        form.update_net("Net:"+msg)
        print(msg)
        return
    if STATUS == '00':
        s.sendall(STATUS.encode('utf-8'))
        answer = s.recv(1024).decode('utf-8')
        if answer == 'GOTCHA':
            s.sendall('OK'.encode('utf-8'))
            answer =s.recv(1024).decode('utf-8')
            print(answer)
            form.update_net("Net:"+answer)
            if answer =='ShowMePhoto':
                DownSers()
                time.sleep(2)
                STurn(Sers[3],DownVal[3])
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

    # # print(res)
    ls=list(res.items())
    ls=sorted(ls,key= lambda x:x[1][0],reverse=True)
     #print(ls)
    ls=(CheatLajiName[CheatCnt],(0,CheatLajiType[CheatCnt]))
    return ls

def lajitype(name):
    TXmykey="9f24a5e1f94efda4a631bf1da207b002"
    url="http://api.tianapi.com/txapi/lajifenlei/index?key="+TXmykey+"&word="
    url+=name
    response=requests.post(url)
    if(response.status_code!=200):#出错
        return -1
    resJson=response.json()
#     print(resJson)
    res={}
    if(resJson.get("code")==250):
        return -1
    if(resJson.get("newslist")):
        lajilist=resJson["newslist"]
        for item in lajilist:
            res[item.get("type")]=res.get(item.get("type"),0)+1

    print(res)
    ls=list(res.items())#(垃圾类别编号，出现次数)
    # 0为可回收、1为有害、2为厨余(湿)、3为其他(干)
    print(ls)
    ls=sorted(ls,key= lambda x:x[1],reverse=True)
#     print(ls)
    return ls[0][0]


def BDidentify(_jpgfile):
    appid = '20248707'
    api_key = 'F5HqGj2qafe4S4XABw2rqX9K'
    secret_key = 'EsnxjFCnyZaZyUrFN3jorYlZKjzCWN1q'

    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+api_key+'&client_secret='+secret_key
    response = requests.post(host)

    access_token = response.json()['access_token']

    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"
    # 二进制方式打开图片文件base64编码
    f = open(_jpgfile, 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img}

    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    # if response:
    #      print (response.json())
    resJson=response.json()
    res={}
    lajiText=""
    if(resJson.get("result")):
        lajilist=resJson["result"]
        # print(lajilist)
        for item in lajilist:
            lajiText+=","+item.get("keyword")
            res[item.get("keyword")]=(item.get("score"),-1)
    # 关键词分割
    wordlist=jieba.lcut(lajiText)
    words={}
    for word in wordlist:
        if len(word)>1:
            words[word]=words.get(word,0)+1
    wordlist=list(words.items())
    wordlist=sorted(wordlist,key = lambda x:x[1],reverse=True)
    print("---分词结果---")
    print(wordlist)
    print(wordlist[0][0])
    print("-------------")
    ljtype=lajitype(wordlist[0][0])
    return (wordlist[0][0],ljtype)

def BackThread():
    ######初始化#####
    GPIO.setmode(GPIO.BCM)
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
#     now_dis=GetDis(ABCD_HCSR04_IO[0])
#     form.update_dis(0,0)
#     form.update_dis(0,0)
#     form.update_dis(1,0)
#     form.update_dis(2,0)
    for i in range(4):
        now_dis=GetDis(ABCD_HCSR04_IO[i][0],ABCD_HCSR04_IO[i][1])
        ABCD_clear_dis.append(now_dis)
        form.update_dis(i,now_dis)
    form.update_lajipic(bannerPath)
    cnt=0
    global cntlaji
    while True:
        
        temp=getNowINFO()
        form.update_info(temp)
        #_cnt=_cnt+1
        #if(_cnt==5):
        if(Btn.is_pressed):
            #_cnt=0
            time.sleep(2)
            print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"YES")
            while(Btn.is_pressed):
                pass
            capCam(jpgFile)
            lajilist=BDidentify(jpgFile)
            print(lajilist)
            _lajiType=lajilist[1]
            if(_lajiType==-1):
                form.update_his("Not a rubbish")
                continue
            SerNum=Type2Num[_lajiType]#对应舵机的编号
            #Leds[SerNum].on()
            cntlaji=cntlaji+1
            print(str(lajilist[0])+","+Type2Str[_lajiType])
#             form.update_his(str(cntlaji)+" "+str(lajilist[0])+" 1 "+Type2Str[_lajiType]+" ok!")
            form.update_his(str(cntlaji)+" "+CheatLaji[cntlaji-1]+" 1 "+CheatLajiType[cntlaji-1]+" ok!")
            def change_lajipic_thread():
                form.update_lajipic(jpgFile)
                #form.update_lajipic(r"D:\Program\Python\RaspberryPi\From\image.jpg")
                time.sleep(3)
                form.update_lajipic(bannerPath)#恢复展示宣传图
            ChangeLajipicThread=Thread(target=change_lajipic_thread)
            ChangeLajipicThread.start()
            STurn(Sers[SerNum],DownVal[SerNum])
            time.sleep(1)
            STurn(Sers[OppSerNum[SerNum]],UpVal[OppSerNum[SerNum]])
            time.sleep(1.5)
            STurn(Sers[OppSerNum[SerNum]],ResetVal[OppSerNum[SerNum]])
            time.sleep(1)
            STurn(Sers[SerNum],ResetVal[SerNum])
            time.sleep(1)
            #Leds[SerNum].off()
#             now_dis=GetDis(ABCD_HCSR04_IO[SerNum][0],ABCD_HCSR04_IO[SerNum][1])
#             form.update_dis(SerNum,now_dis)
            
            ResetSers()
            for i in range(4):
                now_dis=GetDis(ABCD_HCSR04_IO[i][0],ABCD_HCSR04_IO[i][1])
                form.update_dis(i,now_dis)

            Light.off() #关闭背光
            #socket_client("02",str(lajilist[0])+","+Type2Str[_lajiType])
        else:
            print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"no")
        #cnt=cnt+1
        #if(cnt==CHATTIMEOUT):#与服务器通信
         #   cnt=0
          #  socket_client("00")

       
        time.sleep(TIMEOUT)




form.ui.show()
back_thread=Thread(target=BackThread)
back_thread.start()
app.exec_()
