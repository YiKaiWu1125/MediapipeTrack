from asyncio.windows_events import NULL
from os import lstat
from textwrap import indent
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
import math
import time

rx=[]
ry=[]

lx=[]
ly=[]

footrx=[]
footry=[]

footlx=[]
footly=[]

bo=[]

box_index = []
image = NULL

val = 5
z = 0
ba = NULL
bc = NULL
img = NULL

def line_length(ax,ay,bx,by):
    return math.sqrt((ax-bx)**2)+((ay-by)**2)
def line_angle(ax,ay,bx,by,cx,cy):
    dx1 = cx - bx
    dy1 = cy - by
    dx2 = ax - bx
    dy2 = ay - by
    angle1 = math.atan2(dy1, dx1)
    angle1 = -float(angle1 * 180 /math.pi)
    if angle1 < 0:
        angle1 = 360+angle1
    angle2 = math.atan2(dy2, dx2)
    angle2 = -float(angle2 * 180 /math.pi)
    if angle2 < 0:
        angle2 = 360 + angle2
    included_angle = angle1 - angle2
    if abs(included_angle) > 180:
        included_angle=included_angle/abs(included_angle)*(360-abs(included_angle))
    else:
        included_angle*=-1
    if included_angle < 0 :
        included_angle += 360 
    return included_angle
#def print_dot(x,y):
#    cv2.rectangle(image,(x-10,y-10),(x+10,y+10),(0,255,0),5)   # 畫出觸碰區
#    cv2.imshow('MediaPipe Pose', image)
# For webcam input:
cap = cv2.VideoCapture("test.mp4")
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    old = img
    success, img = cap.read()
    if not success:
        #cv2.rectangle(image,(20,20),(500+1,500+1),(0,255,0),5)   # 畫出觸碰區
        #image.flags.writeable = True
        #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        #cv2.imshow('MediaPipe Pose2', image)
        #time.sleep(10)



        print("video end.")
        print("will return the coordinates.")
        print("--------------------------------------------")
        print("right hand (x,y) : ",end="")
        for i in range(len (rx)):
            print("("+str(rx[i])+","+str(ry[i])+") ",end="")
        print("")
        print("--------------------------------------------")
        print("left hand (x,y) : ",end="")
        for i in range(len (lx)):
            print("("+str(lx[i])+","+str(ly[i])+") ",end="")
        print("")
        print("--------------------------------------------\n\n")
        print("Use the resulting trajectory to draw Electrap orbit.\n\n")
        rindex = 1
        for i in range(len (rx)) :
            #bo.append(True)
            if rx[rindex]>rx[i] :
                rindex = i
        box_index.append(rindex)
        last_x = rx[rindex]-1
        last_y = ry[rindex]
        print("begin : "+str(rindex)+" "+str(rx[rindex])+" "+str(ry[rindex]))
        index_len = len(rx)
        while True:
            nowmin = 20000
            nowindex = 1
            for i in range(index_len):
                if i != rindex and (last_x != rx[i] or last_y != ry[i]): #and val >= line_length(rx[rindex],ry[rindex],rx[i],ry[i]):
                    ang = line_angle(last_x,last_y,rx[rindex],ry[rindex],rx[i],ry[i])
                    #print("i: "+str(i) + " and val : "+str(ang)+" "+str(last_x)+","+str(last_y)+","+str(rx[rindex])+","+str(ry[rindex])+","+str(rx[i])+","+str(ry[i]))
                    if(nowmin > ang):
                        nowmin = ang
                        nowindex = i
            if box_index[0] == nowindex :
                print("index : "+ str(nowindex)+ " x: "+ str(rx[nowindex]) + " y: "+str(ry[nowindex]))
                print("go end .")
                break
            else:
                #cv2.rectangle(image,(rx[rindex],ry[rindex]),(rx[nowindex],ry[nowindex]),(255,0,255),5)
                #cv2.imshow('MediaPipe Pose', image)
                box_index.append(nowindex)
                last_x = rx[rindex]
                last_y = ry[rindex]
                rindex = nowindex
                #print("-------------"+str(last_x)+" "+str(last_y)+" "+str(rindex)+" "+str(rx[nowindex])+" "+str(ry[nowindex]))
            print("index : "+ str(nowindex)+ " x: "+ str(rx[nowindex]) + " y: "+str(ry[nowindex]))
        #time.sleep(10)
        print("gmae over")
        # If loading a video, use 'break' instead of 'continue'.
        break
    else:
        image = img
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    size = image.shape   # 取得攝影機影像尺寸
    w = size[1]        # 取得畫面寬度
    h = size[0]        # 取得畫面高度
    if results.pose_landmarks:
        #right hand
        z+=1
        #if(z%4 == 2 ):

        rx.append(int(results.pose_landmarks.landmark[20].x *w))
        ry.append(int(results.pose_landmarks.landmark[20].y *h))
        #left hand
        lx.append(int(results.pose_landmarks.landmark[19].x *w))
        ly.append(int(results.pose_landmarks.landmark[19].y *h))
        #right foot
        footrx.append(int(results.pose_landmarks.landmark[32].x *w))
        footry.append(int(results.pose_landmarks.landmark[32].y *h))
        #left foot
        footlx.append(int(results.pose_landmarks.landmark[31].x *w))
        footly.append(int(results.pose_landmarks.landmark[31].y *h))

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    #hand
    for i in range(len(rx)):
        cv2.rectangle(image,(rx[i]-1,ry[i]-1),(rx[i]+1,ry[i]+1),(0,0,255),5)   # 畫出觸碰區
    for i in range(len(lx)):
        cv2.rectangle(image,(lx[i]-1,ly[i]-1),(lx[i]+1,ly[i]+1),(0,255,0),5)   # 畫出觸碰區
    #foot
    for i in range(len(footrx)):
        cv2.rectangle(image,(footrx[i]-1,footry[i]-1),(footrx[i]+1,footry[i]+1),(255,0,255),5)   # 畫出觸碰區
    for i in range(len(footlx)):
        cv2.rectangle(image,(footlx[i]-1,footly[i]-1),(footlx[i]+1,footly[i]+1),(0,255,255),5)   # 畫出觸碰區
    
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Pose', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()