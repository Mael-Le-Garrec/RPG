import pygame
from pygame.locals import *
import math
import sys
import os

def crop(path, output, size_x, size_y):
    pygame.display.set_mode((1,1), pygame.NOFRAME)
    image = pygame.image.load(path).convert_alpha()

    x = math.ceil(image.get_width()/size_x)
    y = math.ceil(image.get_height()/size_y)

    os.mkdir("./{0}".format(output))
    nb = 0
    for i in range(x):
        for j in range(y):
            screen = pygame.Surface([size_x,size_y], pygame.SRCALPHA, 32).convert_alpha()
            screen.blit(image,(0,0),(i*size_x,j*size_y,size_x,size_y))
            
            if nb < 10:
                pygame.image.save(screen, os.path.join(output,"{0}_00{1}.png".format(output, nb)))
            elif nb < 100:
                pygame.image.save(screen, os.path.join(output,"{0}_0{1}.png".format(output, nb)))
            elif nb < 1000:
                pygame.image.save(screen, os.path.join(output,"{0}_{1}.png".format(output, nb)))
            nb+=1
        
if __name__ == '__main__':
    try:
        texture = sys.argv[1]
        output = sys.argv[2]
    except:
        print("Error : No argument supplied.")
        exit()
    crop(texture, output, 30, 30)