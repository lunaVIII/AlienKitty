import pygame
 
class Kitty:
    """A class to manage the kitty"""
 
    def __init__(self, ak_game):
        """Initialize the kitty and set its starting position"""
        self.screen = ak_game.screen
        self.screen_rect = ak_game.screen.get_rect()
        self.settings = ak_game.settings

        # Load the ship image and get its rectangle
        self.image = pygame.image.load('alien_invasion/images/AlienKitty.png').convert_alpha()
        self.rect = self.image.get_rect()

        # Start each new kitty at the bottom center of the screen
        self.rect.midbottom = (self.screen_rect.centerx, self.screen_rect.bottom - self.settings.margin)

        # Store a float for kittys exact horizontal position
        self.x = float(self.rect.x)

        # Movement flag; start with a kitty thats not moving
        self.moving_right = False
        self.moving_left = False

        self.starting_health = self.settings.max_kitty_health
        self.sound = self.settings.kitty_sound

        self.health = self.starting_health  # Health starts at full

    def blitme(self):
        """Draw the kitty at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update kitty's position based on movement flags"""
        if self.moving_right and self.rect.right < self.screen_rect.right - self.settings.margin:
            self.x += self.settings.kitty_speed
        if self.moving_left and self.rect.left > self.settings.margin:
            self.x -= self.settings.kitty_speed

        self.rect.x = self.x

    def draw_health_bar(self):
        """Draw health bar on the screen."""
        if self.health < 0:
            self.health = 0
        bar_length = 150  # 100 pixels
        bar_height = 20
        fill = (self.health / 3) * bar_length
        health_bar_background = pygame.Rect(self.settings.screen_width - 220, self.settings.screen_height - 80, bar_length, bar_height)
        health_bar_fill = pygame.Rect(self.settings.screen_width - 220, self.settings.screen_height - 80, fill, bar_height)

        pygame.draw.rect(self.screen, (255, 255, 0), health_bar_background)  # Yellow
        pygame.draw.rect(self.screen, (144, 244, 153), health_bar_fill)  # Green 

    def hit_sound(self):
        """Play when kitty is hit"""
        self.sound.play()

    def reset_health(self):
        """Reset kitty health when game restarts"""
        self.health = self.starting_health