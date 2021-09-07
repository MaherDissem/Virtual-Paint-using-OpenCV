import cv2
import numpy as np

def empty(a):
    pass
cv2.namedWindow('TrackBars')
cv2.resizeWindow('TrackBars',640,240)
cv2.createTrackbar('Hue Min', 'TrackBars',0,179,empty)
cv2.createTrackbar('Hue Max', 'TrackBars',179,179,empty)
cv2.createTrackbar('Sat Min', 'TrackBars',0,255,empty)
cv2.createTrackbar('Sat Max', 'TrackBars',255,255,empty)
cv2.createTrackbar('Val Min', 'TrackBars',0,255,empty)
cv2.createTrackbar('Val Max', 'TrackBars',255,255,empty)

def getColor(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    h_min=cv2.getTrackbarPos('Hue Min', 'TrackBars')
    h_max=cv2.getTrackbarPos('Hue Max', 'TrackBars')
    s_min=cv2.getTrackbarPos('Sat Min', 'TrackBars')
    s_max=cv2.getTrackbarPos('Sat Max', 'TrackBars')
    v_min=cv2.getTrackbarPos('Val Min', 'TrackBars')
    v_max=cv2.getTrackbarPos('Val Max', 'TrackBars')

    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])

    mask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow('mask', mask)
    cv2.imshow('Result', imgResult)

    cv2.waitKey(100)
    print(f"h_min={h_min}, h_max={h_max},\n s_min={s_min}, s_max={s_max},\n v_min={v_min}, v_max={v_max}\n\n")

# read webcam
cap = cv2.VideoCapture(0)
cap.set(3,640) # width
cap.set(4,480) # height
cap.set(10,0) # brightness
while True:
    success, img = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q'):   # delay, quit with q
        break
    getColor(img)