import cv2
from sys import exit
from time import sleep
import time
from parser import ArgParser
from IncorrectArgumentsException import *
import csv

SIZE = (640, 480)

def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)


def readCamera(camera):
    (ret, frame) = camera.read()
    return frame


def end(camera=None):
    if camera is not None:
        camera.release()
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

windowName = "OpenCV movement detector"
frames = 50
CPUTIME = time.CLOCK_PROCESS_CPUTIME_ID
	
def main():
    parser = ArgParser(SIZE[0], SIZE[1])
    X1, Y1, X2, Y2 = 0, 0, SIZE[0], SIZE[1]
    try:
    	X1, Y1, X2, Y2 = parser.parse()
    except IncorrectArgumentsException as e:
    	print("ERROR: ", e)
    	end()

    cam = tryInitCamera()

    prev2 = None
    prev2Part = None
    prev = readCamera(cam)
    prevPart = cv2.cvtColor(prev[X1:X2, Y1:Y2], cv2.COLOR_RGB2GRAY)
    curr = readCamera(cam)
    currPart = cv2.cvtColor(curr[X1:X2, Y1:Y2], cv2.COLOR_RGB2GRAY)
    print(currPart[1][1])
    file = open("../results/cv_times.csv", "a")
    size = (X2 - X1) * (Y2 - Y1)
    
    capture = True
    i = 0
    while i < 50:
        i += 1
        prev2Part = prevPart
        prev2 = prev
        prevPart = currPart
        prev = curr
        curr = readCamera(cam)
        
        start_time = time.clock_gettime(CPUTIME)
        currPart = cv2.cvtColor(curr[X1:X2, Y1:Y2], cv2.COLOR_RGB2GRAY)
        
        diff = diffImg(prev2Part, prevPart, currPart)
        end_time = time.clock_gettime(CPUTIME)
        
        elapsed = end_time - start_time
        file.write(str(size) + ", " + str(round(elapsed * 1000000000)) + "\n")
        
        frame = curr.copy()
        frame[X1:X2, Y1:Y2] = cv2.cvtColor(diff, cv2.COLOR_GRAY2RGB)
        cv2.imshow(windowName, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
              break

    file.close()
    end(cam)


if __name__ == '__main__':
    main()


