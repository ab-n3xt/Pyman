import os, sys, pygame

from pygame.locals import *

from Pellet import Pellet
from Pacman import Pacman
from Box import Box

# initialize pygame
pygame.init()
mainClock = pygame.time.Clock()

# constants
WINDOWWIDTH = 448 #(16 * 28) (row numbers range from 0 - 27)
WINDOWHEIGHT = 512 #(16 * 32) (column numbers range from 0 - 31)
SPRITEWIDTH = 16
SPRITEHEIGHT = 16

# initialize window
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)

# initialize colours
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# set background
background = pygame.image.load('../../sprites/pacman-level.png')
windowSurface.blit(background, (0, 0))

# initialize movement variables
moveLeft = False
moveRight = False
moveDown = False
moveUp = False

# pixels per loop
MOVESPEED = 16

# Create Boxes for collisions
box_group = pygame.sprite.Group()

# Pellets
pellet_group = pygame.sprite.Group()

# Teleport
tele_group = pygame.sprite.Group()
tele_group.add(Box(0, 16 * 15, BLUE))
tele_group.add(Box(16 * 27, 16 * 15, BLUE))

# goes through the entire map and outlines which 16x16 areas are black
# and which ones are not
# this identifies where Pacman and Pellets can and cannot spawn
list = [3, 4, 8, 9, 10, 17, 18, 19, 23, 24]
columns = [i * SPRITEWIDTH for i in list]
x = 0
y = 16
while y < WINDOWHEIGHT:
    while x < WINDOWWIDTH:
        selected_area = pygame.Rect(x, y, 16, 16)
        cropped_image = background.subsurface(selected_area)
        if pygame.transform.average_color(cropped_image)[:3] == BLACK:
            if y == SPRITEHEIGHT*4:
                if not x in columns:
                    pellet_group.add(Pellet(selected_area.centerx, selected_area.centery))
            elif not (y >= SPRITEHEIGHT*10 and y <= SPRITEHEIGHT*20):
                pellet_group.add(Pellet(selected_area.centerx, selected_area.centery))
            else:
                if x == SPRITEWIDTH*6 or x == SPRITEWIDTH*21:
                    pellet_group.add(Pellet(selected_area.centerx, selected_area.centery))
        else:
            box_group.add(Box(x, y, RED))
           
        x += 16
    y += 16
    x = 0
    
# create pacman and set coordinates to the center of the surface
pacman = Pacman(224, 384, MOVESPEED, box_group) # 16 * 14, 16 * 24
pacman_group = pygame.sprite.GroupSingle(pacman)

# draw pellets
pellet_group.draw(windowSurface)
pacman_group.draw(windowSurface)

# update display
pygame.display.update()

def update_surface():
    # redraw the background and sprite
    windowSurface.blit(background, (0, 0))
    box_group.draw(windowSurface)
    tele_group.draw(windowSurface)
    pellet_group.draw(windowSurface)
    pacman_group.draw(windowSurface)
    
    # update the game
    pygame.display.update()
    mainClock.tick(10)

def transport(sprite):
    while sprite.rect.left <= WINDOWWIDTH:
        sprite.rect.right += 2
        update_surface()
        
    sprite.rect.right = 0
    
    while sprite.rect.left <= 0:
        sprite.rect.right += 2
        update_surface()
        
    sprite.rect = pygame.Rect(0, 16 * 15, 16, 16)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() 
        if event.type == KEYDOWN:
            if event.key == K_UP:
                moveLeft  = False
                moveRight = False
                moveDown  = False
                moveUp    = True
            if event.key == K_DOWN:
                moveLeft  = False
                moveRight = False
                moveDown  = True
                moveUp    = False
            if event.key == K_LEFT:
                moveLeft  = True
                moveRight = False
                moveDown  = False
                moveUp    = False
            if event.key == K_RIGHT:
                moveLeft  = False
                moveRight = True
                moveDown  = False
                moveUp    = False
                
    # move the sprite(pacman)
    pacman_group.update(moveUp, moveDown, moveLeft, moveRight)
    
    # check if Pacman collided with any Pellets in Pellet Group
    # true = Pellet will be destroyed when collided with
    pygame.sprite.spritecollide(pacman, pellet_group, True)
    
    if pygame.sprite.spritecollide(pacman, tele_group, False):
        transport(pacman)
    
    update_surface()