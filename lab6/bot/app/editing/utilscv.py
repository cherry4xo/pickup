import cv2
import numpy as np
from cvzone import overlayPNG
from svg import make_circle



def rounded(cap: cv2.VideoCapture, size: int, percentage: float):
    out = cv2.VideoWriter("321.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30, (size,size))
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:    
            make_circle(576, 50, "sample", (99, 57, 116), (214, 137, 16), id="123")
            image = cv2.imread(f"123.png")
            size = 576
            img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
            r, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY) 

            roi = frame[-size:, -size:]
            roi[np.where(mask)] = 0
            roi += image 

            frame = cv2.blur(frame, (2, 2))

            out.write(frame)
            if cv2.waitKey(1) == ord("q"):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

cap = cv2.VideoCapture("sample.mp4")
if not cap.isOpened():
    print("Video has not been opened")
rounded(cap=cap, size=576, percentage=0.1)



