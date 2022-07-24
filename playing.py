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
import numpy
import playvideo_getcoor as p_g

video_id = 1#"test1.mp4"
width = 1920
hight = 1080
half_track_width = 25



sta = 'prepare_begin'
game_end_time = 0 
game_begin_time = 0 
x = y = 0

right_hand,binarization_arr=p_g.get_track("test1.mp4")
print("successful get coor.")


def draw(image,right_hand,binarization_arr):
    for i in range (len(right_hand)):
        image = p_g.draw_circle(image,right_hand)
    for i in range(1,len(right_hand)):
        image=p_g.draw_and_save_circle_link_poly(image,right_hand[i-1],right_hand[i],i,binarization_arr,0)
    return image

def draw_view(image,right_hand,binarization_arr,x,y,now_number,sta):
    front = (now_number-2)
    end = (now_number+2)
    if front < 0 :
        front = 0
    if end > len(right_hand):
        end = len(right_hand)-1
    if now_number == len(right_hand)-1 : 
        sta = 'game_over'
        pass
    if now_number == 0 :
        if binarization_arr[0][x][y] == 1:
            now_number = 1
            sta = 'playing'
    else :
        k = True
        for i in range (end,front):
            if binarization_arr[i][x][y] == 0 :
                now_number = i
                k = False
                break
        if k :
            now_number = 0
            sta = 'prepare_begin'
            print("restart")


    if sta != "game_over":
        image = draw(image,right_hand,binarization_arr)   # 畫出電管
    if sta == 'prepare_begin':
        image = cv2.circle(image, (right_hand[0][0],right_hand[0][1]), half_track_width, (0,255,0), -1)# 畫出起始位置框
    if sta == 'playing':
        cv2.circle(image, (right_hand[len(right_hand)-1][0],right_hand[len(right_hand)-1][1]), half_track_width, (0,255,0), -1)   # 畫出終止位置框
    if sta == 'game_over':
        cv2.putText(image, "score:" + str(int(game_end_time - game_begin_time)) + " s.",
                    (0, 150), cv2.FONT_HERSHEY_PLAIN, 5, (260, 25, 240), 3)  # 檢視成績
        cv2.putText(image, "<Game over>", (0, 250),
                    cv2.FONT_HERSHEY_PLAIN, 5, (260, 25, 240), 3)
        cv2.rectangle(image, (155, 280), (420, 330),
                      (0, 25, 240), 5)   # 再玩一次
        cv2.putText(image, "play again", (160, 320),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 25, 240), 3)  # 再玩一次
        cv2.rectangle(image, (155, 350), (420, 400),
                      (0, 25, 240), 5)   # 遊戲結束
        cv2.putText(image, "end game", (160, 390),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 25, 240), 3)  # 遊戲結束
    print("sta is :"+str(sta))
    return image


# For webcam input:
cap = cv2.VideoCapture(video_id)
cap.set(3,width) #設定解析度
cap.set(4,hight) #設定解析度
now_number = 0
with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            break

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = cv2.resize(image,(width,hight))  # 調整畫面尺寸
        results = pose.process(img)
        
        #img = image
        size = img.shape   # 取得攝影機影像尺寸
        w = size[1]        # 取得畫面寬度
        h = size[0]        # 取得畫面高度
        print("w:"+str(w)+" h: "+str(h))

        if results.pose_landmarks:
            x = results.pose_landmarks.landmark[20].x *w#R_DIP].x *w  # 取得食指末端 x 座標
            y = results.pose_landmarks.landmark[20].y *h#mp_hands.HandLandmark.INDEX_FINGER_DIP].y *h  # 取得食指末端 y 座標
            print("y is :"+str(results.pose_landmarks.landmark[20].y))
            x = int(x)
            y = int(y)
            print("x: " +str(x)  + " y : " +str(y))
            re = 1
        else:
            print("no hand.")
        # Draw the hand annotations on the image.
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            img,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        img = draw_view(img,right_hand,binarization_arr,x,y,now_number,sta)

        img=cv2.rectangle(img,(x-10,y-10),(x+10,y+10),(0,150,200),5)   # 畫出觸碰區
        cv2.imshow('MediaPipe Pose', img)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
cv2.destroyAllWindows()
