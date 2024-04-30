import pygame
from pygame.locals import *
from sys import exit
from random import *

## comentários uteis
# x, y = pygame.mouse.get_pos() pega a posiçaõ do mouse


pygame.init()
screen = pygame.display.set_mode((1280, 720))
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    x = 150
    y = 150
    screen.fill((0,0,0))
    
    # órbita mercurio
    pygame.draw.ellipse(screen, (200,200,200), (1280/2,720/2,x,y), 2)

    # órbita venus
    #pygame.draw.ellipse(screen, (200,200,200), (1280/2.1,720/3,x*1.5,y*1.5), 2)
    
    

    
    
    pygame.display.update()

print("a")


print("teste")