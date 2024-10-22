import pygame
import random
from pygame.sprite import Sprite
from projectiles import Projectile

class Octo(Sprite):
    """A class to manage octos"""

    def __init__(self, ak_game, image_path, x, y, octo_type='small'):
        super().__init__()
        self.game = ak_game  # Store reference to the main ak_game instance
        self.settings = ak_game.settings
        self.screen = ak_game.screen
        self.projectiles = ak_game.projectiles
        self.sound = self.settings.blast_sound
        self.octo_type = octo_type
        self.image = pygame.image.load(image_path).convert_alpha()

        if self.octo_type == 'boss':
            self.image = pygame.transform.scale(self.image, (self.settings.boss_alien_size))  # Example: Scale up for boss
            self.original_image = self.image.copy()  # Store original image for reset
            self.max_health = self.settings.max_boss_health
            self.velocity = 1
        else:
            self.image = pygame.transform.scale(self.image, (self.settings.small_alien_size))  # Example: Scale down for minions
            self.original_image = self.image.copy()  # Store original image for reset
            self.max_health = self.settings.max_minion_health
            self.velocity = 0

        self.rect = self.image.get_rect(center=(x, y))
        self.health = self.max_health

        # Random Shooting settings
        self.shoot_delay = random.randint(5000, 10000)  # Initial delay between 5-10 seconds
        self.last_shot_time = pygame.time.get_ticks() - random.randint(0, self.shoot_delay)  # Stagger start times

        # Flash Settings
        self.hit_flash_duration = 10
        self.is_flashing = False
        self.flash_counter = 0

    def update(self):
        """Update the octo's behaviour"""
        # Moving logic
        if self.octo_type == 'boss':
            self.rect.x += self.velocity
            if self.rect.right >= self.settings.screen_width or self.rect.left <= 0:
                self.velocity *= -1  # Change direction

        # Shooting logic
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_delay:
            self.shoot()
            self.last_shot_time = current_time
            self.shoot_delay = random.randint(5000, 10000)  # Reset delay for randomness

        if self.is_flashing:
            self.flash_counter += 1
            if self.flash_counter % 2 == 0:
                self.image.fill((255, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)  # Tint red
            else:
                self.image = self.original_image.copy()  # Reset to original image
            if self.flash_counter >= self.hit_flash_duration:
                self.is_flashing = False
                self.flash_counter = 0
                self.image = self.original_image.copy()  # Ensure image is reset after flashing

    def shoot(self):
        """Create a projectile moving downwards."""
        if self.octo_type == 'boss' or self.octo_type == 'small':
            # Assume projectile moves downwards with direction = 1
            new_projectile = Projectile(self.game, self.rect.centerx, self.rect.bottom)
            self.game.projectiles.add(new_projectile)

    def draw_health_bar(self):
        """Claculations for octo health"""
        self.health_bar_length = self.settings.boss_health_bar_length if self.octo_type == 'boss' else self.settings.minion_health_bar_length  # Length of the health bar in pixels
        self.health_bar_height = self.settings.boss_health_bar_height if self.octo_type == 'boss' else self.settings.minion_health_bar_height # Height of the health bar in pixels
        # Calculate position for the health bar
        if self.octo_type == 'boss':
            # Position it at the center top of the screen
            bar_x = (self.settings.screen_width - self.health_bar_length) // 2
            bar_y = 50  # 20 pixels from the top of the screen
        else:
            # Position it just above the octo for minions
            bar_x = self.rect.x
            bar_y = self.rect.y - self.health_bar_height - 5

        # Draw the background of the health bar
        health_bar_background = pygame.Rect(bar_x, bar_y, self.health_bar_length, self.health_bar_height)
        pygame.draw.rect(self.screen, (255, 0, 0), health_bar_background)  # Red background for lost health

        # Calculate current health bar length
        current_health_length = (self.health / self.max_health) * self.health_bar_length

        # Draw foreground of health bar
        health_bar_foreground = pygame.Rect(bar_x, bar_y, current_health_length, self.health_bar_height)
        pygame.draw.rect(self.screen, (0, 255, 0), health_bar_foreground)  # Green foreground for current health

    def draw(self):
        """Draw the octo on the screen."""
        self.screen.blit(self.image, self.rect)
        self.draw_health_bar()  # Draw health bar when drawing the Octo

    def hit(self):
        """Flash when octo is hit"""
        self.health -= 1
        self.is_flashing = True
        self.flash_counter = 0

    def hit_sound(self):
        """Play when boss octo is defeated"""
        self.sound.play()