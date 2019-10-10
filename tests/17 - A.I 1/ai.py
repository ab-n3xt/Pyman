import os, sys, pygame

from pygame.locals import *

from Pellet import Pellet
from Pacman import Pacman
from Box import Box

# Initialize Pygame
pygame.init()

# Initialize Clock
mainClock = pygame.time.Clock()

# Constants
WINDOWWIDTH = 448 #(16 * 28) (row numbers range from 0 - 27)
WINDOWHEIGHT = 512 #(16 * 32) (column numbers range from 0 - 31)

# Initialize colours
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize window
window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
window.fill(BLACK)

# Pixels per loop
MOVESPEED = 16
    
# Initialize Pacman
pacman = Pacman(224, 384, MOVESPEED) # 16 * 14, 16 * 24
pacman_group = pygame.sprite.GroupSingle(pacman)

# Initialize movement variable
movement = 'R'
last_movement = 'R'

# Draw Pacman onto the window
pacman_group.draw(window)

# Update display
pygame.display.update()

def update_window():
    """Updates the window by redrawing the background and sprites"""

    # Redraw the background and sprites
    pacman_group.draw(window)
    ghost_group.draw(window)
    
    # Update the display
    pygame.display.update()
    mainClock.tick(10)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() 
        if event.type == KEYDOWN:
            if event.key == K_UP:
                movement = 'U'
            if event.key == K_DOWN:
                movement = 'D'
            if event.key == K_LEFT:
                movement = 'L'
            if event.key == K_RIGHT:
                movement = 'R'
                
    pacman_group.update(movement)
    ghost_group.update(movement)
       
    # Transport Pacman if Pacman collides with either transporter
    if pygame.sprite.spritecollide(pacman, l_transporter, False):
        transport_left(pacman)
    elif pygame.sprite.spritecollide(pacman, r_transporter, False):
        transport_right(pacman)
    
    # Update game
    update_window()