import cv2 as cv
import sys
import matplotlib.pyplot as plt

cap=cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    sys.exit(0)
while True:
    ret,frame = cap.read()
    img=cv.cvtColor(frame,1)
    plt.imshow(frame[:,:,::-1])
    plt.show()
    break
cap.release()

