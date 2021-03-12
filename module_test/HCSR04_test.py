import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
TRIG=2
ECHO=3
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
#输出10us的方波脉冲
GPIO.output(TRIG,True)
time.sleep(0.00001)
GPIO.output(TRIG,False)
#等待ECHO的低电平结束
while GPIO.input(ECHO)==0:
    pass
st=time.time()
#等待高电平传回
while GPIO.input(ECHO)==1:
    pass
ed=time.time()
dis=(ed-st)*350*100/2
print(dis)
GPIO.cleanup()

