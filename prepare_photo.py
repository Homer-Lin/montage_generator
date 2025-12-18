import cv2
from datetime import datetime
cap = cv2.VideoCapture('demo_video.mp4')  #被讀取的影片
tem_time = datetime.now()
i = 1

while(True):
    ret, frame = cap.read()
    if not ret:
        print("讀取失敗")
        break

    cv2.imshow('Frame',frame)
    if (datetime.now() - tem_time).total_seconds() > 0.1:
        cv2.imwrite('./img/img_'+str(i)+'.jpg',frame) 
        tem_time = datetime.now()
        i+=1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

