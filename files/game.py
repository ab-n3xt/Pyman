import os, sys, pygame

from pygame.locals import *

from Pellet import Pellet
from Pacman import Pacman
from Box import Box
from Start import Start
from Retry import Retry
from Ghost import Ghost

# Initialize Pygame
pygame.init()

# Initialize Clock
mainClock = pygame.time.Clock()

# Initialize the game's Start Menu
Start()

# Constants
WINDOWWIDTH = 448 #(16 * 28) (row numbers range from 0 - 27)
WINDOWHEIGHT = 512 #(16 * 32) (column numbers range from 0 - 31)
SPRITEWIDTH = 16
SPRITEHEIGHT = 16
LIVES = 3

# Initialize window
window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)

# Initialize colours
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set background
background = pygame.image.load('../sprites/pacman-level.png')
window.blit(background, (0, 0))

# Initialize movement variables
moveLeft = False
moveRight = False
moveDown = False
moveUp = False

# Pixels per loop
MOVESPEED = 4

# Boxes (for collision purposes)
# To create a Box object: Box(x, y, COLOR)
box_group = pygame.sprite.Group()

# Grid (for movement)
# Uses Box objects
grid_group = pygame.sprite.Group()

# Pellets
# To create a Pellet object: Pellet(x, y)
pellet_group = pygame.sprite.Group()

# Teleporters
l_transporter = pygame.sprite.GroupSingle(Box(0, 16 * 15, BLUE))
r_transporter = pygame.sprite.GroupSingle(Box(16 * 27, 16 * 15, BLUE))

# Goes through the entire map and outlines which 16x16 areas are black
# This identifies where Pacman and Pellets can and cannot go
list = [3, 4, 8, 9, 10, 17, 18, 19, 23, 24]
columns = [i * SPRITEWIDTH for i in list]
x = 0
y = 16
while y < WINDOWHEIGHT:
    while x < WINDOWWIDTH:
        # 16x16 area used for cropping
        selected_area = pygame.Rect(x, y, 16, 16)
        
        # Creates a cropped image from the background
        cropped_image = background.subsurface(selected_area)
        
        # If the cropped image's color is BLACK
        if pygame.transform.average_color(cropped_image)[:3] == BLACK:
            # Create grid for movement
            grid_member = Box(x, y, GREEN)
            grid_member.check_possible_moves(x, y)
            grid_group.add(grid_member)
            
            # These if-statements are for specific cases
            if y == SPRITEHEIGHT*4:
                if not x in columns:
                    pellet_group.add(Pellet(selected_area.centerx, selected_area.centery))
            elif not (y >= SPRITEHEIGHT*10 and y <= SPRITEHEIGHT*20):
                pellet_group.add(Pellet(selected_area.centerx, selected_area.centery))
            else:
                if x == SPRITEWIDTH*6 or x == SPRITEWIDTH*21:
                    pellet_group.add(Pellet(selected_area.centerx, selected_area.centery))
           
        x += 16
    y += 16
    x = 0
    
# Initialize Pacman
pacman = Pacman(224, 384, MOVESPEED, box_group) # 16 * 14, 16 * 24
pacman_group = pygame.sprite.GroupSingle(pacman)

# Initialize Ghosts
ghost_group = pygame.sprite.Group()
ghost_group.add(Ghost(208, 384))

# Initialize movement variable
movement = 'R'
last_movement = 'R'

def update_window():
    """Updates the window by redrawing the background and sprites"""

    # Redraw the background and sprites
    window.blit(background, (0, 0))
    pellet_group.draw(window)
    pacman_group.draw(window)
    ghost_group.draw(window)
    
    # Update the display
    pygame.display.update()
    mainClock.tick(40)

def transport_right(sprite):
    """Transports sprite from the right side of the window to the left side"""
    
    while sprite.rect.left <= WINDOWWIDTH:
        sprite.rect.right += 10
        update_window()
        
    sprite.rect.right = 0
    
    while sprite.rect.left <= 0:
        sprite.rect.right += 10
        update_window()
        
    sprite.rect = pygame.Rect(16 * 1, 16 * 15, 16, 16)
    
def transport_left(sprite):
    """Transports sprite from the left side of the window to the right side"""
    
    while sprite.rect.right >= 0:
        sprite.rect.left -= 10
        update_window()
        
    sprite.rect.left = WINDOWWIDTH
    
    while sprite.rect.right >= WINDOWWIDTH:
        sprite.rect.left -= 10
        update_window()
        
    sprite.rect = pygame.Rect(16 * 26, 16 * 15, 16, 16)

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
                
    # Updates Pacman's movement
    current_grid_location = pygame.sprite.spritecollide(pacman, grid_group, False)
    grid_member = current_grid_location.pop()
    if movement in grid_member.valid_moves:
        for x in range(4):
            pacman_group.update(movement)
            update_window()

        last_movement = movement
    else:
        if last_movement in grid_member.valid_moves:
            for x in range(4):
                pacman_group.update(last_movement)
                update_window()
    
    # Check if Pacman collided with any Pellets
    # True = Pellet will be destroyed when collided with
    pygame.sprite.spritecollide(pacman, pellet_group, True)
    
    # check if Pacman collided with any Ghosts
    # If so, check if they are vulnerable
    # If true, destroy the sprite
    # If not, quit the game
    collided_ghosts = pygame.sprite.spritecollide(pacman, ghost_group, False)
    for ghost in collided_ghosts:
        if ghost.isVulnerable:
            ghost.kill()
        else:
            window.fill(BLACK)
            pygame.display.update()
            pacman.death()
            Retry()
    
    # Transport Pacman if Pacman collides with either transporter
    if pygame.sprite.spritecollide(pacman, l_transporter, False):
        transport_left(pacman)
    elif pygame.sprite.spritecollide(pacman, r_transporter, False):
        transport_right(pacman)
    
    # Update game
    update_window()