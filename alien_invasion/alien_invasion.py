# Spencer Augenstein
# Alien Invasion Game
# Fun game project that involves shooting down alien ships. Based on Python Crash Course by Eric Matthes
# Created: 3/26/2025 | Updated: 4/4/2025

# Import libraries and local files
import sys
import pygame
from time import sleep

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Manage assets and behavior"""

# -=-=-=-= ( Run Game ) =-=-=-=-

    def __init__(self):
        """Initialize game"""
        pygame.init()
        self.settings = Settings()
    
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        
        # Create game objects
        self.ship = Ship(self)        
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        # Store and display game statistics
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)
        
        # Create alien fleet
        self._create_fleet()
        
        # Create play button
        self.play_button = Button(self, "Play Game")
        
    def run_game(self):
        """Main game loop"""
        while True:
            self._check_events()

            if (self.stats.game_active):
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _update_screen(self):
        """Update all active screen elements"""
        # Screen properties
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
    
        # Update all bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        
        # Draw scoreboard value
        self.scoreboard.show_score()
    
        # Draw the play button when game is inactive
        if (not self.stats.game_active):
            self.play_button.draw_button()
        
        # Draw most recent screen
        pygame.display.flip()

# -=-=-= ( Check for Keys ) =-=-=- 
          
    def _check_events(self):
        """Check for specific event commands """
        for event in pygame.event.get():
            # Detect if the game should be closed
            if (event.type == pygame.QUIT):
                sys.exit()
            # Detect keypresses
            elif (event.type == pygame.KEYDOWN):
                self._check_keydown_events(event)
            elif (event.type == pygame.KEYUP):
                self._check_keyup_events(event)
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                mouse_position = pygame.mouse.get_pos()
                self._check_click_event(mouse_position)

    def _check_click_event(self, mouse_position):
        """React to mouse click events on buttons"""
        # Start game when player clicks play
        if (self.play_button.rect.collidepoint(mouse_position) and not self.stats.game_active):
            # Reset game state
            self.stats.reset_stats()
            self.settings.dynamic_settings()
            self.aliens.empty()
            self.bullets.empty()
            
            # Create a new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()
            
            # Prepare stats
            self.scoreboard.prepare_score()
            self.scoreboard.prepare_level()
            self.scoreboard.prepare_ships()
            
            # Start game
            self.stats.game_active = True
            
            # Hide mouse cursor
            pygame.mouse.set_visible(False)
        
    def _check_keydown_events(self, event):
        """Detect when keys are pressed"""
        # Ship movement
        if (event.key == pygame.K_LEFT):
            self.ship.moving_left = True
        elif (event.key == pygame.K_RIGHT):
            self.ship.moving_right = True
        # Fire bullets
        elif (event.key == pygame.K_SPACE):
            self._fire_bullet()
        # Quit game
        elif (event.key == pygame.K_q):
            sys.exit()

    def _check_keyup_events(self, event):
        """Stop moving ship when key is released"""
        if (event.key == pygame.K_LEFT):
            self.ship.moving_left = False
        elif (event.key == pygame.K_RIGHT):
            self.ship.moving_right = False

# -=-=-= ( Manage Bullets ) =-=-=-

    def _fire_bullet(self):
        """Fire a bullet if bullets are avalible"""
        if (len(self.bullets) < self.settings.max_bullets):
            spawned_bullet = Bullet(self)
            self.bullets.add(spawned_bullet)
  
    def _update_bullets(self):
        """Update state of active bullets"""
        # Update bullet positions
        self.bullets.update()

        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if (bullet.rect.bottom <= 0):
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()
        
# -=-=-= ( Manage Aliens ) =-=-=-
    
    def _create_fleet(self):
        """Initialize alien fleets"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        avalible_x, avalible_y = alien_width, alien_height
        ship_height = self.ship.rect.height
        
        # Code for first wave
        number_of_rows = (self.settings.screen_width)
        aliens_per_row = ((self.settings.screen_height - (3 * alien_height) - ship_height) // (1 * alien_width))

        if (self.stats.wave == 1):
            for row_number in range(number_of_rows):
                for alien_number in range(aliens_per_row):
                    if (alien_number == row_number or alien_number == (aliens_per_row - row_number - 1)):
                        self._create_alien((alien_width + 2 * alien_width * alien_number), 
                                           ((alien_height + 1 * alien.rect.height * row_number)))
             
        # Code for more waves           
        elif (self.stats.wave >= 2):
            while avalible_y < (self.settings.screen_height - 3 * alien_height):
                while avalible_x < (self.settings.screen_width - 2 * alien_width):
                    self._create_alien(avalible_x, avalible_y)
                    avalible_x += 2 * alien_width
                    
                # Finished a row; reset x value, and increment y value.
                avalible_x = alien_width
                avalible_y += 2 * alien_height
            
    def _create_alien(self, alien_number, row_number):
        """Initialize individual aliens"""
        alien = Alien(self)
    
        # Determine x and y sizes
        alien.x = alien_number
        alien.rect.x = alien_number
        alien.rect.y = row_number
        
        # Officially add the aliens
        self.aliens.add(alien)

    def _change_fleet_direction(self):
        """Drop aliens down a layer"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        # Change alien direction
        self.settings.fleet_direction *= -1
     
    def _update_aliens(self):
        """Update state of active aliens"""
        # Check if alien is on an edge
        self._check_fleet_edges()
        # Update position of all aliens
        self.aliens.update()
        
        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
    
        # Detect when alein hits bottom of the screen
        self._check_aliens_bottom()
     
# -=-=-= ( Manage Collisions ) =-=-=-       
    
    def _check_fleet_edges(self):
        """Check if any aliens hit the playfield border"""
        for alien in self.aliens.sprites():
            if (alien.check_edges()):
                # Drop down and change directions
                self._change_fleet_direction()
                break
            
    def _check_aliens_bottom(self):
        """Check if aliens hit the bottom playfield border"""
        for alien in self.aliens.sprites():
            if (alien.rect.bottom >= self.settings.screen_height):
                # Make ship loose a life
                self._ship_hit()
                break
            
    def _check_bullet_alien_collisions(self):
        """Respond to alien collisions"""
        
        # Check if bullets hit an alien, if so get rid of both
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
                
        # Increase score for all object collisions
        if (collisions):
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points
            self.scoreboard.prepare_score()
            self.scoreboard.prepare_level()
            self.scoreboard.check_high_score()
            
        # Destory existing bullets and create new alien fleet
        if (not self.aliens):
            self.bullets.empty()
            # Increase level
            self.stats.wave += 1
            # Increase game speed and level
            self.settings.increase_speed()
            self.scoreboard.prepare_level()
            # Create fleet
            self._create_fleet()

    def _ship_hit(self):
        """Manage ship properties when it gets hit"""
        if (self.stats.lives_left > 0):
            # Decrease lives by 1.
            self.stats.lives_left -= 1
            self.scoreboard.prepare_ships()

            # Get rid of bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Briefly pause
            sleep(0.5)
        else:
            print("!! Game Over !!")
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


# -=-=-=-=-= ( Run Game ) =-=-=-=-=-
    
if (__name__ == '__main__'):
    
    # Run game instance
    alien = AlienInvasion()
    alien.run_game()
    