import sys
import pygame
import random
import math
from settings import Settings
from kitty import Kitty
from bullet import Bullet
from octo import Octo

class AlienKitty:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()

        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Kitty")
        self.game_over = self.settings.game_over
        self.clock = pygame.time.Clock()

        self._call_sprite_groups()
        self.kitty = Kitty(self)
        self._initialize_octo()
        
        self._play_background_music()

    def _call_sprite_groups(self):
        self.bullets = pygame.sprite.Group()
        self.octo = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

    def _draw_gradient(self):
        """Draw a vertical gradient from start_color to end_color using the instance settings"""
        height = self.settings.screen_height
        width = self.settings.screen_width
        start_color = self.settings.gradient_start_color
        end_color = self.settings.gradient_end_color

        for i in range(height):
            ratio = i / height
            intermediate_color = (
                int(start_color[0] * (1 - ratio) + end_color[0] * ratio),
                int(start_color[1] * (1 - ratio) + end_color[1] * ratio),
                int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            )
            pygame.draw.line(self.screen, intermediate_color, (0, i), (width, i))

        # Simulate stars
        for _ in range(20):  # Adjust number for more/less stars
            star_x = random.randint(0, width)
            star_y = random.randint(0, height)
            pygame.draw.circle(self.screen, (255, 255, 255), (star_x, star_y), 1)  # Small white dots

    def _draw_borders(self):
        """Draw both outer and inner borders."""
        # Draw the outer border
        pygame.draw.rect(
            self.screen, 
            self.settings.outer_border_color, 
            (self.settings.outer_border_thickness // 2, 
            self.settings.outer_border_thickness // 2, 
            self.settings.screen_width - self.settings.outer_border_thickness, 
            self.settings.screen_height - self.settings.outer_border_thickness), 
            self.settings.outer_border_thickness
        )

        # Draw the inner border (inset from the outer border)
        pygame.draw.rect(
            self.screen, 
            self.settings.inner_border_color, 
            (self.settings.outer_border_thickness + self.settings.inner_border_thickness // 2, 
            self.settings.outer_border_thickness + self.settings.inner_border_thickness // 2, 
            self.settings.screen_width - 2 * self.settings.outer_border_thickness - self.settings.inner_border_thickness, 
            self.settings.screen_height - 2 * self.settings.outer_border_thickness - self.settings.inner_border_thickness), 
            self.settings.inner_border_thickness
        )

    def _play_background_music(self):
        """Plays background music indefinitely"""
        pygame.mixer.music.load('alien_invasion/sounds/Space.mp3')
        pygame.mixer.music.set_volume(2.0)  # Adjust volume if needed
        pygame.mixer.music.play(-1)  # Loop indefinitely
    
    def _check_events(self):
        """Respond to key presses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                  self._check_keyup_events(event)
                
    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            # Move kitty to the right
            self.kitty.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Move kitty to the left
            self.kitty.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            pygame.mixer.music.stop()
            sys.exit()
        elif event.key == pygame.K_r and self.game_over:
            self._restart_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            self.settings.bullet_sound.play()

    def _check_keyup_events(self, event):
        """Respond to keyreleases"""
        if event.key == pygame.K_RIGHT:
            self.kitty.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.kitty.moving_left = False

    def load_blast_images(self):
        """Loads and resizes blast images for the animation"""
        self.blast_images = []
        for i in range(1, 4):  # Assuming you have 5 images for the blast sequence
            image = pygame.image.load(f'alien_invasion/images/blast{i}.png').convert_alpha()
            image = pygame.transform.scale(image, self.settings.boss_alien_size)  # Resize image
            self.blast_images.append(image)

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullet group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """Update position of the bullet and check for collisions"""
        # Update bullet position
        self.bullets.update()
        self._check_bullet_octo_collisions()

    def _update_projectiles(self):
        """Update position of the projectiles and check for collisions"""
        # Update projectile position
        self.projectiles.update()
        self._check_projectile_kitty_collisions()

    def _check_bullet_octo_collisions(self):
        """Check for any bullets that have hit octos"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.octo, True, False)
        for octos in collisions.values():
            for octo in octos:
                octo.hit()  # Call hit method, which handles health and flash
                if octo.health <= 0:
                    if octo.octo_type == 'boss':
                        octo.kill()
                        octo.hit_sound()
                        self._start_blast_animation(self.boss_octo.rect.center)
                    else:    
                        octo.kill()

    def _check_projectile_kitty_collisions(self):
        """Check for collisions between projectiles and Kitty"""
        # This checks for collisions and can optionally make the projectiles disappear on hit
        collisions = pygame.sprite.spritecollide(self.kitty, self.projectiles, True)
        if collisions:
            for projectile in collisions:
                # Assuming Kitty has a health attribute
                self.kitty.health -= 1
                self.kitty.hit_sound()
                if self.kitty.health <= 0:
                    self.game_over = True
                    self._handle_kitty_death()

    def _start_blast_animation(self, position):
        """Handle blast animation when boss octo dies"""
        self.load_blast_images()
        self.blast_animation_active = True
        self.blast_animation_position = position
        self.blast_animation_frame = 0

        while self.blast_animation_active and self.blast_animation_frame < len(self.blast_images):
            frame = self.blast_images[self.blast_animation_frame]
            frame_rect = frame.get_rect(center=self.blast_animation_position)
            self.screen.blit(frame, frame_rect)
            self.blast_animation_frame += 1
            pygame.display.flip()  # Update the display to reflect the new frame

            if self.blast_animation_frame >= len(self.blast_images):
                self.blast_animation_active = False  # Stop the animation
            pygame.time.wait(200)  # Wait a bit between frames to make the animation visible

        self.game_over = True
        self._handle_octo_death()

    def _initialize_octo(self):
        self.boss_octo = self._create_boss_octo(self.settings.screen_width / 2, self.settings.screen_height / 2 - 100)  # Centralized boss
        self._create_octo_circle(self.boss_octo, 5)  # Minions in a circle around the boss

    def _create_boss_octo(self, x, y):
        """Boss octo creation"""
        boss_octo = Octo(self, 'alien_invasion/images/AlienOctoBig.png', x, y, octo_type='boss')
        self.octo.add(boss_octo)
        return boss_octo
    
    def _calculate_fixed_radius(self, boss_center_x, boss_center_y, minion_width, minion_height):
        """Calculate minion radius"""
        margin = self.settings.margin
        distances = [
            boss_center_x - margin - minion_width // 2,  # Distance to the left edge
            self.settings.screen_width - boss_center_x - margin - minion_width // 2,  # Distance to the right edge
            boss_center_y - margin - minion_height // 2,  # Distance to the top edge
            self.settings.screen_height - boss_center_y - margin - minion_height // 2  # Distance to the bottom edge
        ]
        return min(distances)

    def _create_octo_circle(self, boss_octo, count):
        """Create minion circle"""
        cx, cy = boss_octo.rect.center
        minion_width = minion_height = self.settings.small_alien_size[0]
        radius = self._calculate_fixed_radius(cx, cy, minion_width, minion_height)

        angle_step = 360 / count if count > 0 else 0
        for i in range(count):
            angle = i * angle_step
            rad_angle = math.radians(angle)
            x = cx + radius * math.cos(rad_angle)
            y = cy + radius * math.sin(rad_angle)

            new_octo = Octo(self, 'alien_invasion/images/AlienOctoSmall.png', x, y, octo_type='small')
            new_octo.angle = angle
            self.octo.add(new_octo)

    def _update_minions(self):
        """Update minions wrt the boss octo"""
        boss_octo = next((o for o in self.octo if o.octo_type == 'boss'), None)
        if boss_octo:
            cx, cy = boss_octo.rect.center
            minion_width = minion_height = self.settings.small_alien_size[0]
            radius = self._calculate_fixed_radius(cx, cy, minion_width, minion_height)

            for octo in (o for o in self.octo if o.octo_type == 'small'):
                octo.angle = (octo.angle + 0.5) % 360
                rad_angle = math.radians(octo.angle)
                octo.rect.x = cx + radius * math.cos(rad_angle) - octo.rect.width / 2
                octo.rect.y = cy + radius * math.sin(rad_angle) - octo.rect.height / 2

        for octo in self.octo:
            octo.update()  # Update all Octos, including the boss which now handles its own movement logic

    def _display_game_over(self, reason):
        """Game over screen when kitty or octo dies"""
        self.game_over_reason = reason
        # Fill the screen with a dark overlay or another appropriate game over background
        self.screen.fill((0, 0, 0))  # Using black for simplicity

        # Set the main game over font size dynamically based on screen height
        self.game_over_font_size = max(40, int(self.settings.screen_height / 10))
        self.instructions_font_size = max(20, int(self.settings.screen_height / 20))  # Smaller font size for instructions

        # Initialize fonts
        self.game_over_font = pygame.font.Font(None, self.game_over_font_size)
        self.instructions_font = pygame.font.Font(None, self.instructions_font_size)

        if self.game_over_reason == 'kitty':
            # Display game over text in the center of the screen
            game_over_text = self.game_over_font.render('GAME OVER!', True, (255, 0, 0))  # Red color

        elif self.game_over_reason == 'octo':
            # Display game over text in the center of the screen
            game_over_text = self.game_over_font.render('OCTO HAS BEEN DEFEATED!', True, (255, 0, 0))  # Red color

        # Additional instructions
        restart_text = self.instructions_font.render('Press "R" to Restart', True, (255, 255, 255))  # White color for visibility
        quit_text = self.instructions_font.render('Press "Q" to Quit', True, (255, 255, 255))  # White color

        game_over_rect = game_over_text.get_rect(center=(self.settings.screen_width / 2, self.settings.screen_height / 2 - self.game_over_font_size))
        restart_rect = restart_text.get_rect(center=(self.settings.screen_width / 2, self.settings.screen_height / 2))
        quit_rect = quit_text.get_rect(center=(self.settings.screen_width / 2, self.settings.screen_height / 2 + self.instructions_font_size))

        # Blit the texts onto the screen
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(restart_text, restart_rect)
        self.screen.blit(quit_text, quit_rect)

        pygame.display.flip()

        self._check_events()

    def _restart_game(self):
        """Reset the game"""
        # Reset game states
        self.game_over = False
        # Reset all necessary attributes and game entities
        self.kitty.reset_health()
        self.octo.empty()
        self.bullets.empty()
        self.projectiles.empty()
        # Reinitialize the game state or reload the level
        self.boss_octo = self._create_boss_octo(self.settings.screen_width / 2, self.settings.screen_height / 2 - 100)
        self._create_octo_circle(self.boss_octo, 5)

    def _handle_octo_death(self):
        """Handle octo death"""
        self._display_game_over('octo')

    def _handle_kitty_death(self):
        """Handle kitty death"""
        self._display_game_over('kitty')

    def _update_game(self):
        """Handle all update methods"""
        self.kitty.update()
        self._update_bullets()
        self._update_minions()
        self._update_projectiles()

    def _draw_game_elements(self):
        """Draw all the game elements"""
        self.kitty.blitme()
        self.kitty.draw_health_bar()
        for bullet in self.bullets:
            bullet.draw_bullet()
        for octo in self.octo:
            octo.draw()
        for projectile in self.projectiles:
            projectile.draw_projectile()

    def _render_objects(self):
        """Render everything on the screen"""
        # Draw the gradient background first
        self._draw_gradient()
        # Draw the inner and outer borders
        self._draw_borders()
        self._draw_game_elements()
        pygame.display.flip()

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            # Watch for keyboard and mouse events
            self._check_events()
            if not self.game_over:
                self._update_game()
                self._render_objects()
            else:
                self._display_game_over(self.game_over_reason)
                continue
            self.clock.tick(60)

if __name__ == '__main__':
    # Make a game instance, and run the game
    ak = AlienKitty()
    ak.run_game()