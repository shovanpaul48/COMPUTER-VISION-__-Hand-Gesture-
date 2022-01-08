import math
import cv2
import time
import numpy as np
import HandTrackingModule as htm

# pycaw modules
# https://github.com/AndreMiras/pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def main():
    loop=0
    while loop < 5: 
        x = int(input(" what  you want to do \n1.Open webcam  \n2.Open a recorded video \n"))
        if x==1:
            cam = cv2.VideoCapture(0)
            break
        elif x==2:
            path = str(input("Enter the file path : "))
            cam = cv2.VideoCapture(path)
            break
        else:
            loop +=1
            print("You entered a wrong choise , Select again" )
    # set Resolution of the video cam
    h_cam,w_cam = 1200,720
    cam.set(3, w_cam)
    cam.set(4, h_cam)
    pTime = 0
    detector = htm.hand_detect(detectionCon=0.7)

    # pycaw ------------------------------------------
    #pycaw module allows us to control volume of the pc

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # volume.GetMute()
    # volume.GetMasterVolumeLevel()
    volRange = volume.GetVolumeRange()
    # volume.SetMasterVolumeLevel(-10, None)

    #set variables-----------------------------------
    minVol = volRange[0]
    maxVol = volRange[1]
    vol=0
    volBAR =400
    volPer = 0
    try : 
        while True:
            success, img = cam.read()
            img = detector.find_hand(img)
            lmlist = detector.find_hand_posistion(img)
            if len(lmlist) != 0:
                print(lmlist[4],lmlist[8])

                #index fingertip landmark  [4][1] 
                p, q = lmlist[4][1],lmlist[4][2]
                # and thumb finger landmark is [8][1]
                r, s = lmlist[8][1],lmlist[8][2]
                # calculate the center of index and thumb finge
                center_x,center_y= (p+r)//2, (q+s)//2
                #  draw the circles
                cv2.circle(img,(p,q),8,(255,200,0),cv2.FILLED)
                cv2.circle(img,(r,s),8,(255,200,0),cv2.FILLED)
                cv2.line(img,(p,q),(r,s),(255,200,0),3)
                cv2.circle(img,(center_x,center_y),12,(255,200,0),cv2.FILLED)

                length = math.hypot(r-p,s-q) # it calculates the square root between two cordinates
                #  hand range is 50 - 250
                #  volume range is  -65  - 0
                
                # interp() function returns the one-dimensional piecewise linear interpolant 
                # to a function with given discrete data points (xp, fp), evaluated at x. 
                # Parameters : x : [array_like] The x-coordinates at which to evaluate the interpolated values.
                vol = np.interp(length,[50,250],[minVol,maxVol])   
                volBAR = np.interp(length,[50,250],[350,150])
                volPer = np.interp(length,[50,250],[0,100])
                # print("volPer : " ,volPer)
                volume.SetMasterVolumeLevel(vol,None)
                if(length < 50 ):                                                                  
                    cv2.circle(img,(center_x,center_y),12,(100,255,0),cv2.FILLED)

                cv2.putText(img, f'{int(volPer)}%', (50, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 200, 0), 2)  
                
                # drawing the volume bar 
                cv2.rectangle(img,(50,130),(85,350),(100,230,0),2)
                cv2.rectangle(img,(50,int(volBAR)),(85,350),(230,150,0),2,cv2.FILLED)
                cTime = time.time()
                fps = 1 / (cTime-pTime)
                pTime = cTime
                cv2.putText(img, f'FPS:{int(fps)}', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 200, 0), 2)


            cv2.imshow("Cam Video",img)
            cv2.waitKey(1)

    except Exception as e:
        print("An error occur : ", e)


if __name__ == "__main__":
    main()
