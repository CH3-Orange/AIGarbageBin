# 按钮按下之后执行函数的测试
from gpiozero import Button

def testoutput():
    print("push down!")

btn=Button(3)
btn.when_pressed=testoutput