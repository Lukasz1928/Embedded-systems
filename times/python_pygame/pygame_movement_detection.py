import pygame
import pygame.camera
from pygame import Surface
from pygame.locals import *
from sys import exit
from time import sleep
import time
import timeit
from parser import ArgParser
from copy import copy

SIZE = (640, 480)

def tryInitCamera():
    pygame.init()
    print("Initializing camera", end='', flush=True)
    for i in range(0, 10):
        pygame.camera.init()
        print(".", end='', flush=True)
        cam_ids = pygame.camera.list_cameras()
        if len(cam_ids) > 0:
            print("\rCamera initialized succesfully")
            return pygame.camera.Camera(cam_ids[0], SIZE, "RGB")
        sleep(1)
    print("\rCamera could not be initialized")
    end()
    
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

    camera = tryInitCamera()
    
    display = pygame.display.set_mode(SIZE, 0)

    camera.start()
    screen = pygame.surface.Surface(SIZE, 0, display)
    capture = True

    prev2 = None
    prev2Part = None
    prev  = camera.get_image()
    prevPart = toGrayscale(prev, tl=(X1, Y1), br=(X2, Y2))
    curr = camera.get_image()
    currPart = toGrayscale(curr, tl=(X1, Y1), br=(X2, Y2))
    
    file = open("../results/pg_times.csv", "a")
    size = (X2 - X1) * (Y2 - Y1)
    
    i = 0
    while i < frames:
        i += 1
        prev2 = prev
        prev2Part = prevPart
        prev = curr
        prevPart = currPart
        curr = camera.get_image()
        
        start_time = time.clock_gettime(CPUTIME)
        currPart = toGrayscale(curr, tl=(X1, Y1), br=(X2, Y2))
        diff = diffImg(prev2Part, prevPart, currPart, tl=(X1, Y1), br=(X2, Y2))
        end_time = time.clock_gettime(CPUTIME)
        
        elapsed = end_time - start_time
        file.write(str(size) + ", " + str(round(elapsed * 1000000000)) + "\n")
        
        frame = copy(curr)
        frame.blit(diff, (X1, Y1))
        display.blit(frame, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_q:
                capture = False
                break
    file.close()
    end(camera)

def end(camera=None):
    if camera is not None: 
        camera.stop()
    pygame.quit()
    print("Program ended")
    exit()   

def toGrayscale(screen, tl=(0, 0), br=SIZE):
    result = Surface((br[0] - tl[0], br[1] - tl[1]))
    for i in range(tl[0], br[0]):
        for j in range(tl[1], br[1]):
            pixel = screen.get_at((i,j))
            grayValue = toGray(pixel)
            pixel = (grayValue, grayValue, grayValue)
            result.set_at((i - tl[0],j - tl[1]), pixel)
    return result

def diffImg(t0, t1, t2, tl=(0, 0), br=SIZE):
    d1 = absdiff(t2, t1, tl=tl, br=br)
    d2 = absdiff(t1, t0, tl=tl, br=br)
    return bitwise_and(d1, d2, tl=tl, br=br)

def pixelDiff(p1, p2):
    result = Color(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]), abs(p1[2] - p2[2]), round(abs(p1[3] + p2[3]) / 2))
    return result

def absdiff(s1, s2, tl=(0, 0), br=SIZE):
    result = Surface((br[0] - tl[0], br[1] - tl[1]))
    for i in range(tl[0], br[0]):
        for j in range(tl[1], br[1]):
            result.set_at((i - tl[0], j - tl[1]), pixelDiff(s1.get_at((i - tl[0], j - tl[1])), s2.get_at((i - tl[0], j - tl[1]))))
    return result

def bitwise_and(s1, s2, tl=(0, 0), br=SIZE):
    result = Surface((br[0] - tl[0], br[1] - tl[1]))
    for i in range(tl[0], br[1]):
        for j in range(tl[1], br[1]):
            c = s1.get_at((i - tl[0], j - tl[1]))[0] & s2.get_at((i - tl[0], j - tl[1]))[0]
            result.set_at((i - tl[0], j - tl[1]), Color(c, c, c))
    return result
	
			
def toGray(pixel):
    grayValue = round(0.2989 * pixel[0] + 0.5870 * pixel[1] + 0.1140 * pixel[2])
    return grayValue


if __name__ == '__main__':
    main()
