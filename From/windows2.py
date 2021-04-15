import ENV
from PySide2.QtWidgets import QApplication, QMessageBox,QLabel,QWidget,QMainWindow,QDialog
from PySide2 import QtUiTools,QtCore
from threading import Thread
from PySide2.QtGui import QPixmap,QCloseEvent
from PySide2.QtCore import QFile,QThread,Signal,QObject
from PIL import Image
import matplotlib.pyplot as plt
import time,base64,json,requests
import socket,os,sys,struct,time
import raspberryPi as rasp

if ENV.__ENV__=="RaspberryPi":
    # jpgFile='image.png'
    # bannerPath=r"/home/pi/Desktop/AIGarbageBin/From/jpg/banner0.png"
    # PicBasePath=r'/home/pi/Desktop/AIGarbageBin/From/jpg'
    uiPath=r'/home/pi/Desktop/AIGarbageBin/From/ui/windows2_ui.ui'
elif ENV.__ENV__=="Windows":
    # jpgFile='From\image.png'
    # bannerPath=r"D:\Program\Python\RaspberryPi\AIGarbageBin\From\jpg\banner0.png"
    # PicBasePath=r'D:\Program\Python\RaspberryPi\AIGarbageBin\From\jpg'
    uiPath=r'D:\Program\Python\RaspberryPi\AIGarbageBin\From\ui\windows2_ui.ui'

SertoInt={"左上":0,"左下":1,"右上":2,"右下":3,"全部":-1}
HCSRtoInt={"左上":0,"左下":1,"右上":2,"右下":3}

# class UiLoader(QtUiTools.QUiLoader):
#     _baseinstance = None

#     def createWidget(self, classname, parent=None, name=''):
#         if parent is None and self._baseinstance is not None:
#             widget = self._baseinstance
#         else:
#             widget = super(UiLoader, self).createWidget(classname, parent, name)
#             if self._baseinstance is not None:
#                 setattr(self._baseinstance, name, widget)
#         return widget

#     def loadUi(self, uifile, baseinstance=None):
#         self._baseinstance = baseinstance
#         widget = self.load(uifile)
#         QtCore.QMetaObject.connectSlotsByName(widget)
#         return widget


class Form2(QMainWindow):
    
    def __init__(self):
        super(Form2,self).__init__()
        
        self.ui = QtUiTools.QUiLoader().load(uiPath)
        
        # self.ui.show()
        # self.ui=UiLoader().loadUi(uiPath)
        # self.setWindowTitle("设置")
        self.ui.UpdateSers_IO.clicked.connect(self.UpdateSers_IO_clicked)

        self.ui.ParaSerGo.clicked.connect(self.ParaSerGo_clicked)
        self.ui.ParaSerSave2Up.clicked.connect(self.ParaSerSave2Up_clicked)
        self.ui.ParaSerSave2Reset.clicked.connect(self.ParaSerSave2Reset_clicked)
        self.ui.ParaSerSave2Down.clicked.connect(self.ParaSerSave2Down_clicked)

        self.ui.quitBtn.clicked.connect(self.closeEvent)

        self.ui.CtrlSerUp.clicked.connect(self.CtrlSerUp_clicked)
        self.ui.CtrlSerReset.clicked.connect(self.CtrlSerReset_clicked)
        self.ui.CtrlSerDown.clicked.connect(self.CtrlSerDown_clicked)

        self.ui.UpdateHCSR_IO.clicked.connect(self.UpdateHCSR_IO_clicked)
        self.ui.HCSRGo.clicked.connect(self.HCSRGo_clicked)
        self.ui.FlagEmptyDis.clicked.connect(self.FlagEmptyDis_click)
        self.ui.FlagFullDis.clicked.connect(self.FlagFullDis_click)
        # self.ui.UpdateOpenBtn_IO.clicked.connect(self.UpdateOpenBtn_IO_clicked)

        # self.ui.closeEvent=closeEvent
        self.reflash()

    def closeEvent(self):
        ENV.blockFlag=0
        self.ui.close()
        
    def reflash(self):
        '''
        刷新页面，主要是更新界面上IO口的显示
        '''
        #舵机IO
        self.ui.SerLeftUp_IO.setValue(rasp.ABCD_SERVO_IO[0])
        self.ui.SerLeftDown_IO.setValue(rasp.ABCD_SERVO_IO[1])
        self.ui.SerRightUp_IO.setValue(rasp.ABCD_SERVO_IO[2])
        self.ui.SerRightDown_IO.setValue(rasp.ABCD_SERVO_IO[3])
        #HCSR04 超声波IO
        self.ui.TrigLeftUp_IO.setValue(rasp.ABCD_HCSR04_IO[0][0])
        self.ui.EchoLeftUp_IO.setValue(rasp.ABCD_HCSR04_IO[0][1])

        self.ui.TrigLeftDown_IO.setValue(rasp.ABCD_HCSR04_IO[1][0])
        self.ui.EchoLeftDown_IO.setValue(rasp.ABCD_HCSR04_IO[1][1])

        self.ui.TrigRightUp_IO.setValue(rasp.ABCD_HCSR04_IO[2][0])
        self.ui.EchoRightUp_IO.setValue(rasp.ABCD_HCSR04_IO[2][1])
        
        self.ui.TrigRightDown_IO.setValue(rasp.ABCD_HCSR04_IO[3][0])
        self.ui.EchoRightDown_IO.setValue(rasp.ABCD_HCSR04_IO[3][1])

        # self.ui.OpenBtn_IO.setValue(rasp.OpenBtn_IO)


    def UpdateSers_IO_clicked(self):
        '''
            更新舵机IO口
        '''
        SerLeftUpIO=self.ui.SerLeftUp_IO.value()
        SerLeftDownIO=self.ui.SerLeftDown_IO.value()
        SerRightUpIO=self.ui.SerRightUp_IO.value()
        SerRightDownIO=self.ui.SerRightDown_IO.value()
        # MessageBox=QMessageBox()
        # MessageBox.information(self.ui,"LeftUpIO",str(LeftUpIO))
        rasp.ABCD_SERVO_IO[0]=SerLeftUpIO
        rasp.ABCD_SERVO_IO[1]=SerLeftDownIO
        rasp.ABCD_SERVO_IO[2]=SerRightUpIO
        rasp.ABCD_SERVO_IO[3]=SerRightDownIO
        self.reflash()
        rasp.InitSers()
    
    def GetChoseSerAndPara(self):
        '''
        获取ParaChooseSer中的舵机，旋转ParaSerRotate参数，注意进行参数范围判断
        '''
        ParaChooseSer=self.ui.ParaChooseSer.currentText()
        ParaSerRotate=self.ui.ParaSerRotate.value()
        try:
            chose=SertoInt[ParaChooseSer]
        except Exception as e:
            MessageBox=QMessageBox()
            MessageBox.critical(self.ui,"错误",repr(e))
            return None,None

        if chose<0 or chose>3:
            MessageBox=QMessageBox()
            MessageBox.critical(self.ui,"错误","不在范围内的选择："+str(chose))
            return None,None
        if ParaSerRotate<-1 or ParaSerRotate>1:
            MessageBox=QMessageBox()
            MessageBox.critical(self.ui,"错误","不在范围内(-1~1)的旋转角度："+str(chose))
            return None,None
        return chose,ParaSerRotate
    def ParaSerGo_clicked(self):
        '''
             对选中的舵机进行旋转 调树莓派的Sturn
        '''
        ser,para=self.GetChoseSerAndPara()
        if ser==None or para==None:
            return
        rasp.STurn(rasp.Sers[ser],para)
    def ParaSerSave2Up_clicked(self):
        '''
            保存配置为当前舵机的上升参数
        '''
        ser,para=self.GetChoseSerAndPara()
        if ser==None or para==None:
            return
        rasp.UpVal[ser]=para
        print("UpVal"+str(rasp.UpVal))
    def ParaSerSave2Reset_clicked(self):
        '''
            保存配置为当前舵机的待机参数
        '''
        ser,para=self.GetChoseSerAndPara()
        if ser==None or para==None:
            return
        rasp.ResetVal[ser]=para
        print("ResetVal"+str(rasp.ResetVal))
    def ParaSerSave2Down_clicked(self):
        '''
            保存配置为当前舵机的下降参数
        '''
        ser,para=self.GetChoseSerAndPara()
        if ser==None or para==None:
            return
        rasp.DownVal[ser]=para
        print("DownVal"+str(rasp.DownVal))

    def GetChoseSer(self):
        '''
        获取CtrlChooseSer中的舵机，注意进行参数范围判断
        '''
        CtrlChooseSer=self.ui.CtrlChooseSer.currentText()
        try:
            chose=SertoInt[CtrlChooseSer]
        except Exception as e:
            MessageBox=QMessageBox()
            MessageBox.critical(self.ui,"错误",repr(e))
            return None

        if chose<-1 or chose>3:
            MessageBox=QMessageBox()
            MessageBox.critical(self.ui,"错误","不在范围内的选择："+str(chose))
            return None
        return chose
    def CtrlSerUp_clicked(self):
        '''
            控制选择的舵机向上
        '''
        ser=self.GetChoseSer()
        if ser==None or ser==-1:
            MessageBox=QMessageBox()
            MessageBox.critical(self.ui,"错误","不能所有挡板同时抬起")
            return
        else:
            rasp.STurn(rasp.Sers[ser],rasp.UpVal[ser])
    def CtrlSerReset_clicked(self):
        '''
            控制选择的舵机向上
        '''
        ser=self.GetChoseSer()
        if ser==None:
            MessageBox=QMessageBox()
            MessageBox.critical(self.ui,"错误","参数范围外的舵机"+str(ser))
        elif ser==-1:
            rasp.ResetSers()
        else:
            rasp.STurn(rasp.Sers[ser],rasp.ResetVal[ser])
    def CtrlSerDown_clicked(self):
        '''
            控制选择的舵机向上
        '''
        ser=self.GetChoseSer()
        if ser==None:
            MessageBox=QMessageBox()
            MessageBox.critical(self.ui,"错误","参数范围外的舵机"+str(ser))   
        elif ser==-1:
            rasp.DownSers()
        else:
            rasp.STurn(rasp.Sers[ser],rasp.DownVal[ser])
    
    def UpdateHCSR_IO_clicked(self):
        rasp.ABCD_HCSR04_IO[0]=(self.ui.TrigLeftUp_IO.value()
                                ,self.ui.EchoLeftUp_IO.value())

        rasp.ABCD_HCSR04_IO[1]=(self.ui.TrigLeftDown_IO.value()
                                ,self.ui.EchoLeftDown_IO.value())

        rasp.ABCD_HCSR04_IO[2]=(self.ui.TrigRightUp_IO.value()
                                ,self.ui.EchoRightUp_IO.value())
        
        rasp.ABCD_HCSR04_IO[3]=(self.ui.TrigRightDown_IO.value()
                                ,self.ui.EchoRightDown_IO.value())

        self.reflash()
    def GetChoseHCSR(self):
        '''
        获取ChooseHCSR的超声波传感器，注意进行参数范围判断
        '''
        ChooseHCSR=self.ui.ChooseHCSR.currentText()
        try:
            chose=HCSRtoInt[ChooseHCSR]
        except Exception as e:
            MessageBox=QMessageBox()
            MessageBox.critical(self.ui,"错误",repr(e))
            return None

        if chose<0 or chose>3:
            MessageBox=QMessageBox()
            MessageBox.critical(self.ui,"错误","不在范围内的选择："+str(chose))
            return None
        return  chose
    def HCSRGo_clicked(self):
        '''
            对选择的超声波传感器进行探测
        '''
        chose=self.GetChoseHCSR()
        if chose == None:
            return
        dis=rasp.GetDis(rasp.ABCD_HCSR04_IO[chose][0],rasp.ABCD_HCSR04_IO[chose][1])
        self.ui.DisReturn.setText(str(dis))
    def FlagEmptyDis_click(self):
        num_str=self.ui.DisReturn.text()
        try:
            num=float(num_str)
        except Exception as e:
            MessageBox=QMessageBox()
            MessageBox.critical(self.ui,"数值转换错误",repr(e))
            return
        chose=self.GetChoseHCSR()
        if chose == None:
            return
        rasp.ABCD_empty_dis[chose]=num
        print("EmptyDis"+str(rasp.ABCD_empty_dis))

    def FlagFullDis_click(self):
        num_str=self.ui.DisReturn.text()
        try:
            num=float(num_str)
        except Exception as e:
            MessageBox=QMessageBox()
            MessageBox.critical(self.ui,"数值转换错误",repr(e))
            return
        chose=self.GetChoseHCSR()
        if chose == None:
            return
        rasp.ABCD_full_dis[chose]=num
        print("FullDis"+str(rasp.ABCD_full_dis))
    
    def UpdateOpenBtn_IO_clicked(self):
        newOpenBtn_IO=self.ui.OpenBtn_IO.currentText()
        rasp.OpenBtn_IO=newOpenBtn_IO
        rasp.InitOpenBtn()
        self.reflash()

if __name__ == '__main__':
    app = QApplication([])
    form2 = Form2()
    form2.ui.show()
    # app.aboutToQuit.connect(form2.closeEvent)
    sys.exit(app.exec_())