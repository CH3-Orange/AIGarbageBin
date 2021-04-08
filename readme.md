# 智能分拣垃圾箱代码说明

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


