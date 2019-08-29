import pygame

from pygame.locals import *

class Pacman(pygame.sprite.Sprite):
    
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        
        self.surface = pygame.display.get_surface()
        
        self.image = pygame.image.load('../../sprites/pacman.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        self.speed = speed
        
    def update(self, moveLeft, moveRight, moveDown, moveUp):
        if moveLeft and self.rect.left > 0:
            self.rect.left -= self.speed
            
        if moveRight and self.rect.right < self.surface.get_width():
            self.rect.right += self.speed
            
        if moveDown and self.rect.bottom < self.surface.get_height():
            self.rect.bottom += self.speed
            
        if moveUp and self.rect.top > 0:
            self.rect.top -= self.speed