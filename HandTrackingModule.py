import cv2
import mediapipe as mp
import time
import threading 

# Hand Tracking Class
class hand_detect():
    stop = 1
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        #by default dtection percentage is set to 50% ,  user can increease and decrease it while create an object of the class 
        self.trackCon = trackCon
        #by default tracking percentage is set to 50% ,  user can increease and decrease it while create an object of the class 
        # traking is easier than detection . So we always perform detection first
        
        self.mpHands = mp.solutions.hands
        # self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        
    
    # detection of hand 
    def find_hand(self,img,draw=True):
        self.imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(self.imgRGB)
        # print(results.multi_hand_landmarks)
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)
            
        return img
    
    # traking of the hand
    def find_hand_posistion(self,img,handNo=0,draw=True):
        landmark_list = [] # it will store all the land marks  while tracking 
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for hand_id, landmark in enumerate(myHand.landmark):
                # print(hand_id, landmark)
                height, width , channel = img.shape 
                center_x_axis, centre_y_axis = int(landmark.x*width) , int(landmark.y*height)
                # print(hand_id,center_x_axis,centre_y_axis)
                landmark_list.append([hand_id,center_x_axis,centre_y_axis])
                if draw:
                    cv2.circle(img,(center_x_axis,centre_y_axis),6,(200,200,120),cv2.FILLED)
                    # cv2.line(img,(center_x_axis,centre_y_axis),7,(120,100,120),cv2.FILLED)
        return landmark_list
    
        
 
def main():
    pTime=0
    cTime=0
    loop=0
    while loop < 5: 
        x = int(input(" what  you want to do \n1.Open webcam  \n2.Open a recorded video \n"))
        if x==1:
            vid_img = cv2.VideoCapture(0)
            break
        elif x==2:
            path = str(input("Enter the file path : "))
            vid_img = cv2.VideoCapture(path)
            break
        else:
            loop +=1
            print("You entered a wrong choise , Select again" )
            
    try:
        loop=0
        detector = hand_detect()
        
        while True:
            # if loop==30:
            #     t1 = threading.Thread()
            #     stop = int(input("If you want to stop then enter 0  else 1 : "))
            #     detector.stop=stop
            
            loop+=1
            success , img = vid_img.read()
            img = detector.find_hand(img)
            handlist = detector.find_hand_posistion(img)
            
            cTime= time.time()
            fps = 1/(cTime-pTime)
            pTime=cTime  
            # put the FPS on the video   
            cv2.putText(img,f'FPS:{int(fps)}',(50,50),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),2)
            
            cv2.imshow("Image",img)
            if(detector.stop  == 1 ):  
                cv2.waitKey(1)
            else:
                 break
    except Exception as e:
        print("An error occur : ", e)

    

if __name__ == "__main__":
    main()
