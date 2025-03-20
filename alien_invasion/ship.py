import pygame

class Ship:
    """Class to manage the ship"""
    
    # Note: Rect stands for rectangle
    def __init__(self, ai_game):
        # Initilize ship and its starting position
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        
        # Load ship image
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        
        # Start ship at the bottom center of the field
        self.rect.midbottom = self.screen_rect.midbottom
        
        # Movement flags
        self.moving_left = False
        self.moving_right = False
        
    def update(self):
        # Update ship's position based on movement flag
        if self.moving_left:
            self.rect.x -= 1    
        elif self.moving_right:
            self.rect.x += 1    
    
    def blitme(self):
        # Draw ship at its current location
        self.screen.blit(self.image, self.rect)
        