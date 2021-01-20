import numpy as np
import cv2 as cv
cap = cv.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output1.avi', fourcc, 20.0, (640,  480))

#face = cv.CascadeClassifier('/home/pi/Projects/haarcascade_frontalface_alt2.xml')
#face = cv.CascadeClassifier('C:/Users/73916/Desktop/cp-vton/haarcascade_frontalface_alt2.xml')
face = cv.CascadeClassifier('D:/Download/cp-vton/haarcascade_frontalface_alt2.xml')
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    faces = face.detectMultiScale(frame,scaleFactor=1.1,minNeighbors=5,minSize=(10,10))
    for (x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #print(x,y)

    # write the flipped frame
    out.write(frame)
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break
# Release everything if job is finished
cap.release()
out.release()
cv.destroyAllWindows()