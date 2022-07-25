#import cv2
#import numpy as np
#
#cap = cv2.VideoCapture("test1.avi")  # 创建一个 VideoCapture 对象
#wi = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
#hi = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
#print("first Image Size: %d x %d" % (wi, hi))
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320) #設定解析度
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240) #設定解析度
#wi = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
#hi = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
#print("set over Image Size: %d x %d" % (wi, hi))
#
#
# 
#flag = 1  # 设置一个标志，用来输出视频信息
#
#while(cap.isOpened()):  # 循环读取每一帧
#
#    ret, frame = cap.read()
#    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#    # cv2.imshow("Gray", gray)
# 
#    cv2.imshow("Capture_Test", frame)  # 窗口显示，显示名为 Capture_Test
#    
#    k = cv2.waitKey(1) & 0xFF  # 每帧数据延时 1ms，延时不能为 0，否则读取的结果会是静态帧
#    if k == ord('s'):  # 若检测到按键 ‘s’，打印字符串
#
#        print(cap.get(3))
#        print(cap.get(4))
#        #保存一帧图片
#        cv2.imwrite('1.jpg', frame)
# 
#    elif k == ord('q'):  # 若检测到按键 ‘q’，退出
#        break
# 
#cap.release()  # 释放摄像头
#cv2.destroyAllWindows()  # 删除建立的全部窗口
for i in range(5,1-1,-1):
    print(i)