from PIL import Image
import matplotlib.pyplot as plt
import picamera
import time
camera = picamera.PiCamera()

def cap():
    camera.capture('image.jpg')
    img=Image.open('image.jpg')
    plt.imshow(img)
    plt.show()
    plt.close()
def main():
    
    camera.brightness = 75
    cap()
main()