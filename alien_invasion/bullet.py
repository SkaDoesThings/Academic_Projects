import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):

    def __init__(self, game):
        super().__init__()
        
        self.screen = game.screen
        self.settings = game.settings
        self.color = self.settings.bullet_color
        
        # Create bullet rectangle at (0, 0) and set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = game.ship.rect.midtop
        
        # Store bullet's position as a decimal value
        self.y = float(self.rect.y)

    def update(self):
        # Update decimal position of bullet
        self.y -= self.settings.bullet_speed
        # Update rectangle position
        self.rect.y = self.y
        
    def draw_bullet(self):
        # Draw bullet on the screen
        pygame.draw.rect(self.screen, self.color, self.rect)