import cv2

for i in range(3):
    cap = cv2.VideoCapture(i)
    if cap.read()[0]:
        print(f"Camera index {i} works")
        cap.release()
    else:
        print(f"Camera index {i} failed")
