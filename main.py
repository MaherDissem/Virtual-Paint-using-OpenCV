import cv2
import numpy as np

Colors = [ # h_min,s_min,v_min,h_max,s_max_v_max
    [0,110,0,197,255,255], # red
    [110,113,0,124,193,110], # blue
]
ColorValues = [ # BGR
    [0,0,255],
    [255,0,0]
]


def getContours(img):
    """ 
        draws bounding boxes on the drawing pencil
        and returns its coordinates
    """
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # img, retrieval method
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>300: 
            # draw contours
            cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)
            # length of contour
            peri = cv2.arcLength(cnt,True) 
            # corner points
            corners = cv2.approxPolyDP(cnt,0.02*peri,True) 
            # bounding box
            objCor = len(corners) 
            x,y,w,h = cv2.boundingRect(corners)
            cv2.rectangle(imgResult,(x,y),(x+w,y+h),(0,255,0),3)

            mask = img
            cv2.rectangle(mask,(x,y),(x+w,y+h),(0,255,0),3)
            cv2.imshow('mask', img)
    return x+w//2,y # pencil tip


def findColor(img):
    """ 
        finds the coordinates of the pencil(s) and returns them
    """
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    newPoints = []
    for i, color in enumerate(Colors):
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])

        mask = cv2.inRange(imgHSV,lower,upper)
        x,y = getContours(mask)
        cv2.circle(imgResult,(x,y),10,ColorValues[i],cv2.FILLED) # circle around the pencil tip

        if x!=0 and y!=0:
            newPoints.append([x,y,i])

    return newPoints


def draw(Points):
    for point in Points:
        cv2.circle(imgResult,(point[0],point[1]),10,ColorValues[point[2]],cv2.FILLED)


# read webcam
cap = cv2.VideoCapture(0)
cap.set(3,640) # width
cap.set(4,480) # height
cap.set(10,0) # brightness

Points = [] # x, y, colorId

while True:
    success, img = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q'):   # delay, quit with q
        break
    if cv2.waitKey(1) & 0xFF == ord('s'):   # 
        Points = []
        print("drawing reset")
    
    # img to draw on
    imgResult = img.copy()

    # new points to be added on each frame
    newPoints = findColor(img)
    if len(newPoints)>0:
        for newP in newPoints:
            Points.append(newP)

    # all points since the begining
    if len(Points)>0:
        draw(Points)

    cv2.imshow('result',imgResult)
    cv2.waitKey(10)



