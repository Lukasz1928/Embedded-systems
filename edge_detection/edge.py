import cv2
from sys import exit
import sys
from time import sleep
import numpy as np
from parser import ArgParser

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
    parser = ArgParser()
    arg = parser.parse()
    cam = tryInitCamera()
    winName = "OpenCV edge detector"
    capture = True
    while capture:
        img = readCamera(cam)
        #img = cv2.imread('elephant.jpg', 1)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        if arg == 'canny':
            med = np.median(img)
            s = 0.33
            lower = int(max(0, (1 - s) * med))
            upper = int(max(0, (1 - s) * med))
            img = cv2.Canny(img, lower, upper)
        elif arg == 'sobel':
            img = cv2.Sobel(img, cv2.CV_8U, 1, 1, ksize=3)
        elif arg == 'scharr':
            kx = np.array([[-3, 0, 3], [-10, 0, 10], [-3, 0, 3]])
            ky = np.array([[-3, -10, -3], [0, 0, 0], [3, 10, 3]])
            kxy = np.array([[-6, -10, 0], [-10, 0, 10], [0, 10, 6]])
            img = cv2.filter2D(img, cv2.CV_8U, kxy) 
        elif arg == 'laplacian':
            img = cv2.Laplacian(img, cv2.CV_8U, ksize=3)
        cv2.imshow(winName, img)
        #cv2.imwrite('scharrxy.jpg', img)
        #exit()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            capture = False

    end(cam, winName)


if __name__ == "__main__":
    main()
