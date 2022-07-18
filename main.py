import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

rx=[]
ry=[]

lx=[]
ly=[]

footrx=[]
footry=[]

footlx=[]
footly=[]
# For webcam input:
cap = cv2.VideoCapture("test.mp4")
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
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

        # If loading a video, use 'break' instead of 'continue'.
        break

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
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()