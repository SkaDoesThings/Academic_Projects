import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        
        # Load alien image and set rectangle
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        
        # Start each new alien around top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # Store alien's exact positions
        self.x = float(self.rect.x)