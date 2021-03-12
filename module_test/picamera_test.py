from PIL import Image
import matplotlib.pyplot as plt
import picamera
import time
camera = picamera.PiCamera()
camera.brightness = 70
camera.capture('image.jpg')
img=Image.open('/home/pi/Desktop/image.jpg')
plt.axis("off")
plt.imshow(img)
plt.show()
plt.close()