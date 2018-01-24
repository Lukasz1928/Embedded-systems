import cv2
from sys import exit
import sys
import os
from time import sleep
import numpy as np

def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)


def readCamera(camera):
    (ret, frame) = camera.read()
    return frame


def end(camera, window=None):
    if camera is not None:
        camera.release()
    if window is not None:
        cv2.destroyWindow(window)
    sleep(0.5)
    print("Program ended")
    exit()


def tryInitCamera():
    print("Initializing camera", end='', flush=True)
    for i in range(0, 10):
        camera = cv2.VideoCapture(0)
        print(".", end='', flush=True)
        if camera.isOpened():
            print("\rCamera initalized succesfully")
            return camera
        sleep(1)
    print("\rCamera could not be initialized")
    end()


def main():
    os.chdir(sys.path[0])
    cam = tryInitCamera()
    face_cascade_front = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    winName = "OpenCV face detector"
    capture = True
    while capture:
        img = readCamera(cam)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces_front = face_cascade_front.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces_front:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)      
        cv2.imshow(winName, img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            capture = False

    end(cam, winName)


if __name__ == "__main__":
    main()
