# Spencer Augenstein
# Alien Invasion Game
# Fun game project that involves shooting down alien ships. Based on Python Crash Course by Eric Matthes
# Created 3/19/2025 | Updated: 3/19/2025

# Import libraries and local files
import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    """Manage assets and behavior"""

    def __init__(self):
        """Initialize game"""
        pygame.init()
        self.settings = Settings()
    
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        
        self.ship = Ship(self)        
        self.bullets = pygame.sprite.Group()

        
    def run_game(self):
        """Main game loop"""
        while True:
           self._check_events()
           self.ship.update()
           self.bullets.update()
           self._update_screen()
           
    def _check_events(self):
        """Check for specific event commands """
        for event in pygame.event.get():
            # Detect if the game should be closed
            if event.type == pygame.QUIT:
                sys.exit()
            # Detect keypresses
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Detect when keys are pressed"""
        # Ship movement
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        # Fire bullets
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        # Quit game
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Stop moving ship when key is released"""
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    def _fire_bullet(self):
        spawned_bullet = Bullet(self)
        self.bullets.add(spawned_bullet)

    def _update_screen(self):
        # Screen properties
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
    
        # Update all bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
    
        # Draw most recent screen
        pygame.display.flip()

if __name__ == '__main__':
    # Run game instance
    alien = AlienInvasion()
    alien.run_game()
    