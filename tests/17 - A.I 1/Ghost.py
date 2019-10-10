import pygame

from pygame.locals import *

class Ghost(pygame.sprite.Sprite):

    def __init__(self, x, y, speed):
        # Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        
        # Get the main window's display
        self.surface = pygame.display.get_surface()
        
        # Get the sprite and set the x+y coordinates
        self.image = pygame.image.load('../../sprites/red.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Set Vulnerable state to False
        self.isVulnerable = False
        
        self.speed = speed
        
    def update(self, coordinates):
        x = coordinates[0]
        y = coordinates[1]
        
        distance = 
        
    