import sys

import pygame

from settings import Settings
from ship import Ship

class AlienInvasion:
    """Manage assets and behavior"""

    def __init__(self):
        """Initialize game"""
        pygame.init()
        self.settings = Settings()
    
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        
        self.ship = Ship(self)        
        
    def run_game(self):
        """Game loop"""
        while True:
           self._check_events()
           self.ship.update()
           self._update_screen()
           
    def _check_events(self):
        # Check for specific commands
        for event in pygame.event.get():
            # Detect if the game should be closed
            if event.type == pygame.QUIT:
                sys.exit()
                
            # Move ship while key is pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                elif event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                    
            # Stop moving ship when key is released
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.ship.moving_left = False
                elif event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False

    def _update_screen(self):
        # Screen properties
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
    
        # Draw most recent screen
        pygame.display.flip()
    
if __name__ == '__main__':
    # Run game instance
    alien = AlienInvasion()
    alien.run_game()
    