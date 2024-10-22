import pygame
from pygame.sprite import Sprite

class Projectile(Sprite):
    """A class to manage projectiles fired by thhe octos"""

    def __init__(self, ak_game, x, y): # Direction should be passed, e.g., 1 for down, -1 for up
        super().__init__()
        self.screen = ak_game.screen
        self.settings = ak_game.settings

        # Setup projectile appearance
        self.image = pygame.Surface((self.settings.projectile_size * 2, self.settings.projectile_size * 2))
        self.image.fill((0, 0, 0))  # Fill with transparent color if needed
        self.image.set_colorkey((0, 0, 0))  # Set transparency
        pygame.draw.circle(self.image, self.settings.projectile_color, (self.settings.projectile_size, self.settings.projectile_size), self.settings.projectile_size)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # Store projectile position as float
        self.y = float(self.rect.y)

    def update(self):
        self.y += self.settings.projectile_speed
        self.rect.y = int(self.y)

        if self.rect.top >= self.settings.screen_height - self.settings.margin - self.settings.outer_border_thickness - 2 * self.settings.inner_border_thickness:
            self.kill()

    def draw_projectile(self):
        """Draw the projectile on the screen"""
        self.screen.blit(self.image, self.rect)
