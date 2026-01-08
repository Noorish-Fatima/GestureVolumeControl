import cv2 
import mediapipe as mp
import time 
import numpy as np
import HandTrackingModule as htm
import math 
import os

cap=cv2.VideoCapture(0)
pTime=0

detector=htm.HandDetector()
volume=0
volumeBar=400
volumePer=0
while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img,False)
    if len(lmList)!=0:
        #print(lmList[4],lmList[8])
        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),2)
        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)

        length=math.hypot(x2-x1,y2-y1)
        #print(length)

        #Hand Range 50,300
        volume=np.interp(length,[50,300],[0,100])
        volumeBar=np.interp(length,[50,300],[400,150])
        volumePer = np.interp(length,[50,300],[0,100])
        print(int(length),volume)
        os.system(f"osascript -e 'set volume output volume {volume}'")

        if length<50:
             cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)

    cv2.rectangle(img,(50,150),(85,400),(0,255,0))
    cv2.rectangle(img,(50,int(volumeBar)),(85,400),(0,255,0),cv2.FILLED)
    cv2.putText(img,f'{int(volumePer)}%',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)



    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS: {int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
    cv2.imshow("image",img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break 
cap.release()
cv2.destroyAllWindows()
