import cv2
from sys import exit
import sys
from time import sleep


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
    cam = tryInitCamera()
    winName = "OpenCV movement detector"
    prev2 = None
    prev = cv2.cvtColor(readCamera(cam), cv2.COLOR_RGB2GRAY)
    curr = cv2.cvtColor(readCamera(cam), cv2.COLOR_RGB2GRAY)
    capture = True
    while capture:
        prev2 = prev
        prev = curr
        curr = cv2.cvtColor(readCamera(cam), cv2.COLOR_RGB2GRAY)
        cv2.imshow(winName, diffImg(prev2, prev, curr))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            capture = False

    end(cam, winName)


if __name__ == "__main__":
    main()
