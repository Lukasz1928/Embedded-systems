import pygame
import pygame.camera
from pygame.locals import *
from sys import exit
from time import sleep
import time
import timeit
from parser import ArgParser
from copy import copy

SIZE = (640, 480)
X1, Y1, X2, Y2 = 0, 0, SIZE[0], SIZE[1]

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

def main():
    parser = ArgParser(SIZE[0], SIZE[1])
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
    prev  = toGrayscale(camera.get_image())
    curr = toGrayscale(camera.get_image())
    while capture:
        prev2 = prev
        prev = curr
        image = camera.get_image()
        curr = toGrayscale(image)
        diff = diffImg(prev2, prev, curr)
        display.blit(diff, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_q:
                capture = False
                break
    end(camera)

def end(camera=None):
    if camera is not None: 
        camera.stop()
    pygame.quit()
    print("Program ended")
    exit()   

def toGrayscale(screen):
    for i in range(X1, X2):
        for j in range(Y1, Y2):
            pixel = screen.get_at((i,j))
            grayValue = toGray(pixel)
            pixel = (grayValue, grayValue, grayValue)
            screen.set_at((i,j), pixel)
    return screen

def diffImg(t0, t1, t2):
    d1 = absdiff(t2, t1)
    d2 = absdiff(t1, t0)
    #return d2
    return bitwise_and(d1, d2)

def pixelDiff(p1, p2):
    result = Color(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]), abs(p1[2] - p2[2]), round((p1[3] + p2[3]) / 2))
    return result

def absdiff(s1, s2):
    result = s1
    for i in range(X1, X2):
        for j in range(Y1, Y2):
            result.set_at((i, j), pixelDiff(s1.get_at((i, j)), s2.get_at((i, j))))
    return result

def bitwise_and(s1, s2):
    result = copy(s1)
    for i in range(X1, X2):
        for j in range(Y1, Y2):
            c = s1.get_at((i, j))[0] & s2.get_at((i, j))[0]
            print(str(s1.get_at((i, j))[0]) + " " + str(s2.get_at((i, j))[0]) + " " + str(c))
            result.set_at((i, j), Color(c, c, c))
    return result
	
			
def toGray(pixel):
    grayValue = round(0.2989 * pixel[0] + 0.5870 * pixel[1] + 0.1140 * pixel[2])
    return grayValue


if __name__ == '__main__':
    main()
