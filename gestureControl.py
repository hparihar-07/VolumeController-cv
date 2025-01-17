import cv2
import time
import numpy as np
import Hand_Tracking_Module as hm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
pTime = 0
cTime =0

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(10,100)
detector = hm.handDetector(detectionCon=0.75)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volpercent = 0



while True:
    success, img=cap.read()
    img=detector.findHands(img)
    PosList = detector.findPosition(img,draw=False)
    if len(PosList) != 0:
        # print(lmList[4],lmList[8])
        x1,y1 = PosList[4][1],PosList[4][2]
        x2, y2 = PosList[8][1], PosList[8][2]
        cx,cy = (x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        length = math.hypot(x2-x1,y2-y1 )
        # print(length)

        vol = np.interp(length,[30,150],[minVol,maxVol])
        volBar = np.interp(length, [30, 150], [400, 150])
        volpercent = np.interp(length, [30, 150], [0, 100])
        # print(vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length < 30:
            cv2.circle(img, (cx, cy), 10, (255,0,0), cv2.FILLED)
    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)

    cv2.rectangle(img,(50,int(volBar)),(85,400),(0,150,0),cv2.FILLED)
    cv2.putText(img, f'{str(int(volpercent))}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 3)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (40, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 231, 167), 3)

    cv2.imshow("video",img)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
