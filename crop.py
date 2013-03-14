import pygame
from pygame.locals import *
import math

def crop(path, output, size_x, size_y):
    pygame.display.set_mode((1,1), pygame.NOFRAME)
    image = pygame.image.load(path).convert_alpha()

    x = math.ceil(image.get_width()/size_x)
    y = math.ceil(image.get_height()/size_y)

    nb = 0
    for i in range(x):
        for j in range(y):
            screen = pygame.Surface([size_x,size_y], pygame.SRCALPHA, 32).convert_alpha()
            screen.blit(image,(0,0),(i*size_x,j*size_y,size_x,size_y))
            pygame.image.save(screen, "{0}_{1}.png".format(output, nb))
            nb+=1
        
if __name__ == '__main__':
    crop("maison.png", "maison", 30, 30)