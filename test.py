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
cap = cv2.VideoCapture("test.mp4")
while cap.isOpened():
    success, img = cap.read()
    if not success:
        break
    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()