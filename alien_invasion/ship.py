import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Class to manage the ship"""

    def __init__(self, game):
        """Initialize ship and set starting positoon"""
        super().__init__()
        
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
        
        # Store decimal value for the ship's positions
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
                
        # Movement flags
        self.moving_left = False
        self.moving_right = False
        self.on_left_wall = False
        self.on_right_wall = False

    def update(self):
        # Universal movement method
        def move_ship(dx, dy):
            self.x += dx * self.settings.ship_speed   
            self.y += dy * self.settings.ship_speed 
        
        # Switch to the left wall on contact
        if (self.rect.left == 0):
            self.on_left_wall = True
            move_ship(1, -1)
            
        # Switch to the right wall on contact
        elif (self.rect.right == self.screen_rect.right):
            self.on_right_wall = True
            move_ship(1, -1)
             
        # Leave the corresponding wall
        elif (self.rect.bottom >= self.screen_rect.bottom):
            if (self.on_left_wall == True):
                self.on_left_wall = False 
                move_ship(1, -1)

            elif (self.on_right_wall == True):
                self.on_right_wall = False 
                move_ship(-1, -1)
            
        # Update ship's position based on movement flag using position values
        # Also check position to prevent ship from moving past the window.    
            
        # Default left and right movement
        if (self.on_left_wall == False and self.on_right_wall == False):     
            if (self.moving_left and self.rect.left > 0):
                move_ship(-1, 0)
            elif (self.moving_right and self.rect.right < self.screen_rect.right):
                move_ship(1, 0)
        
        # Movement when on left wall        
        elif (self.on_left_wall == True):
            if (self.moving_left and self.rect.top > 0):
                move_ship(0, -1)
            elif (self.moving_right and self.rect.bottom < self.screen_rect.bottom):
                move_ship(0, 1)
        
        # Movement when on right wall
        elif (self.on_right_wall == True):
            if (self.moving_left and self.rect.bottom < self.screen_rect.bottom):
                move_ship(0, 1)
            elif (self.moving_right and self.rect.top > 0):
                move_ship(0, -1)
            
        # Update rect object from the self.position values
        self.rect.x = self.x
        self.rect.y = self.y
    
    def blitme(self):
        # Variable that allows for modifications to the image
        final_image = self.image
        
        # Flip the ship image based on its current wall
        if (self.on_left_wall == True):
            final_image = pygame.transform.rotate(self.image, -90)
        if (self.on_right_wall == True):
            final_image = pygame.transform.rotate(self.image, 90)

        # Draw ship at its current location
        self.screen.blit(final_image, self.rect)
        
    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)