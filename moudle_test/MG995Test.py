import time
import RPi.GPIO as GPIO

def gpio_init():  #初始化GPIO，设置初始角和信号输出口36
    
    global pwm
    global num_
    global angle
    angle = 90
    num_ = 0
    GPIO.setmode(GPIO.BCM)
    #GPIO.setup(40,GPIO.IN)
    GPIO.setup(23, GPIO.OUT)
    pwm = GPIO.PWM(23, 50)
    pwm.start(10 / 180 * 90 + 2)
    pwm.ChangeDutyCycle(0)  #清空占空比，这句是防抖关键句，如果没有这句，舵机会狂抖不止


def setDirection(direction):  
    duty = 10 / 180 * direction + 2
    pwm.ChangeDutyCycle(duty)
    print("direction =", direction, "-> duty =", duty)   
    time.sleep(1) #等待控制周期结束
    pwm.ChangeDutyCycle(0)   #清空占空比，这句是防抖关键句，如果没有这句，舵机会狂抖不止
    
gpio_init()
while True:
    d=input()
    setDirection(eval(d))
GPIO.cleanup()
