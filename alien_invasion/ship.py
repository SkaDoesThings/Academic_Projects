import pygame

class Ship:
    """Class to manage the ship"""
    
    # Note: Rect stands for rectangle
    def __init__(self, game):
        # Initilize game scren for ship 
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        
        # Initilize ship settings
        self.settings = game.settings

        # Load ship image
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        
        # Start ship at the bottom center of the field
        self.rect.midbottom = self.screen_rect.midbottom
        
        # Store decimal value for the ship's horizontal position
        self.x = float(self.rect.x)
                
        # Movement flags
        self.moving_left = False
        self.moving_right = False
        
    def update(self):
        # Update ship's position based on movement flag using position values
        if self.moving_left:
            self.x -= self.settings.ship_speed    
        elif self.moving_right:
            self.x += self.settings.ship_speed
    
        # Update rect object from the self.position values
        self.rect.x = self.x
        
    def blitme(self):
        # Draw ship at its current location
        self.screen.blit(self.image, self.rect)
        