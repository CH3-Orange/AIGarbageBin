# 智能分拣垃圾箱代码说明

<<<<<<< HEAD
### 文件组织结构图

├─From
│  │  image.jpg		*摄像头捕捉到的图片*

│  │  windows.py		*主程序代码*

│  │  

│  ├─jpg

│  │      banner0.jpg		*宣传图*

│  │      blue0.png			*下面是各垃圾桶在0--5级容量的展示图片*

│  │      blue1.png

│  │      blue2.png

│  │      blue3.png

│  │      blue4.png

│  │      blue5.png

│  │      Error.png

│  │      green0.png

│  │      green1.png

│  │      green2.png

│  │      green3.png

│  │      green4.png

│  │      green5.png

│  │      red0.png

│  │      red1.png

│  │      red2.png

│  │      red3.png

│  │      red4.png

│  │      red5.png

│  │      yellow0.png

│  │      yellow1.png

│  │      yellow2.png

│  │      yellow3.png

│  │      yellow4.png

│  │      yellow5.png

│  │      

│  └─ui

│          windows_ui.ui		*UI文件*

│          

└─module_test

autoChangePic.py		*好像没写完？*
        BDidentify.py			*百度API接口的识别函数*
        CheckCPU.py			*获取CPU温度*
        HCSR04_test.py		*HCSR04超声波传感器测试代码*
        JPGToBase64.py		*JPG文件Base64编码测试代码*
        MainCode.py			*老版本的主程序*
        NewMainCode.py		*老版本的主程序*
        NewMG995.py		*MG995舵机的测试代码*
        NNewMainCode.py		*不接可视化窗口的主程序*
        picamera_test.py		*摄像头测试程序*
        Qt_test.py			*pySide2测试程序*
        RaspberryClient_Fin.py	*树莓派连接服务器客户端测试代码*
        RegOrd.py			*注册表测试代码*
        sensTesst.py			*红外热释电传感器测试代码，目前已弃用传感器方案*
        SG90test.py			*SG90舵机测试代码*
        TXidentify.py			*天行API接口识别函数*
        zipJPG.py			*JPG压缩测试代码*
        

其中From为窗体的主要程序及资源文件夹，module_test文件夹为测试程序文件夹

=======
*----2021.4.4 update----*

重构了主要代码，把原来windows.py内的功能函数分类整理到raspberryPi.py和Identifi.py中，完成了基本要求

*----2021.4.8 update----*

新增了windows2窗口用于调参，以及设置了后台线程的阻塞和终止状态。
完善了满载检测的方法（还有待在树莓派上实测）

**TODOList**

- [ ] 可以播放视频
- [x] 可以弹出页面进行调参
- [x] 完成满载检测及报警
- [ ] 优化垃圾分类算法
- [ ] 把配置保存为配置文件，每次初始化的时候从配置文件初始化

## 重构说明

为了方便在windows和树莓派两个平台进行调试，新增了ENV.py文件，文件中的 *\_\_ENV\_\_* 变量表示是当前处在哪一个平台环境，与c语言中的条件编译类似。
>>>>>>> f53759334b0ebe072dfc005f5a8217d32f6b5627


