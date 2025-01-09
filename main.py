import pygame
import sys
from player import Player
from alien import Alien
from random import choice
from laser import Laser


class Game:
    def __init__(self):
        # Player
        player_sprite = Player(
            pos=(screen_width/2, screen_height/2), size=(45, 45), constraintx=screen_width, constrainty=screen_height, speed=6)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Alien Laser
        self.alien_shoot_timer = pygame.time.get_ticks()
        self.alien_shoot_interval = 1000
        self.alien_laserSpeed = 4
        self.alien_speed = 1

        # health and score
        self.lives = 3
        self.live_surf = pygame.image.load(
            '../SpaceInvaders/graphics/heart.png').convert_alpha()
        heart_width = 30
        heart_height = 30
        self.live_surf = pygame.transform.scale(
            self.live_surf, (heart_width, heart_height))
        self.live_x_start_pos = self.live_surf.get_size()[0] + 25
        self.transparency_timer = 0
        self.heart_visible = True
        self.score = 0
        self.font = pygame.font.Font(None, 20)
        self.highscore = 0
        # Start Screen
        self.game_started = False

        # Alien
        self.aliens = pygame.sprite.Group()
        self.alien_setup1(rows=2, cols=6, offset=(
            (screen_width-340)/2, 20))
        self.alien_setup2(rows=2, cols=6, offset=(
            (screen_width-340)/2, screen_height-90))
        self.alien_setup3(rows=6, cols=2, offset=((
            10, (screen_height-340)/2,)))
        self.alien_setup4(rows=6, cols=2, offset=((
            screen_width-100, (screen_height-340)/2,)))
        self.alien_direction = 1
        self.alien_lasers = pygame.sprite.Group()

    def alien_setup1(self, rows, cols, offset, size=(40, 30), rotation=0):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * (size[0] + 20) + offset[0]
                y = row_index * (size[1] + 20) + offset[1]
                if col == 2 or col == 3:
                    alien_sprite = Alien('pink', x, y, size, rotation)
                else:
                    alien_sprite = Alien('green', x, y, size, rotation)
                self.aliens.add(alien_sprite)

    def alien_setup2(self, rows, cols, offset, size=(40, 30), rotation=180):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * (size[0] + 20) + offset[0]
                y = row_index * (size[1] + 20) + offset[1]
                if col == 2 or col == 3:
                    alien_sprite = Alien('pink', x, y, size, rotation)
                else:
                    alien_sprite = Alien('green', x, y, size, rotation)
                self.aliens.add(alien_sprite)

    def alien_setup3(self, rows, cols, offset, size=(40, 30), rotation=90):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * (size[1] + 20) + offset[0]
                y = row_index * (size[0] + 20) + offset[1]
                if row == 2 or row == 3:
                    alien_sprite = Alien('pink', x, y, size, rotation)
                else:
                    alien_sprite = Alien('green', x, y, size, rotation)
                self.aliens.add(alien_sprite)

    def alien_setup4(self, rows, cols, offset, size=(40, 30), rotation=270):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * (size[1] + 20) + offset[0]
                y = row_index * (size[0] + 20) + offset[1]
                if row == 2 or row == 3:
                    alien_sprite = Alien('pink', x, y, size, rotation)
                else:
                    alien_sprite = Alien('green', x, y, size, rotation)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = self.alien_speed
            elif (alien.rotation_angle == 90 and alien.rect.top >= screen_height-40) or (alien.rotation_angle == 270 and alien.rect.bottom <= 0+40):
                self.alien_direction = self.alien_speed
            elif alien.rect.left <= 0:
                self.alien_direction = -self.alien_speed
            elif (alien.rotation_angle == 90 and alien.rect.bottom <= 0+40) or (alien.rotation_angle == 270 and alien.rect.top >= screen_height-40):
                self.alien_direction = -self.alien_speed

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())

        # Laser
            if random_alien.rotation_angle == 0:  # Downward
                angle = 0
            elif random_alien.rotation_angle == 90:   # Upward
                angle = 90
            elif random_alien.rotation_angle == 180:    # Left
                angle = 180
            elif random_alien.rotation_angle == 270:   # Right
                angle = 270

        # Create and add the laser sprite with direction
            laser_sprite = Laser(random_alien.rect.center, self.alien_laserSpeed, 'red',
                                 screen_height, screen_width, angle)
            self.alien_lasers.add(laser_sprite)

    def collision_check(self):
        for laser in self.player.sprite.lasers:
            if pygame.sprite.spritecollide(laser, self.aliens, True):
                laser.kill()
                self.score += 100
        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    self.transparency_timer = pygame.time.get_ticks()
                    self.heart_visible = True
                    if self.lives <= 0:
                        self.game_started = False
                        self.gameover_screen()
        if self.aliens:
            for alien in self.aliens:
                # pygame.sprite.spritecollide(alien, self.player, True)
                if pygame.sprite.spritecollide(alien, self.player, False):
                    self.lives = 0
                    self.game_started = False
                    self.gameover_screen()

    def display_lives(self):
        current_time = pygame.time.get_ticks()

        # Show the heart only if it's within the display duration
        if self.heart_visible and current_time - self.transparency_timer < 3000:  # 500 ms duration
            for live in range(self.lives):
                x = self.live_x_start_pos + \
                    (live * self.live_surf.get_size()[0] + 10)
                screen.blit(self.live_surf, (x, 8))
        else:
            self.heart_visible = False  # Hide the heart after the duration

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft=(0, 0))
        screen.blit(score_surf, score_rect)

    def start_screen(self):
        square_size = 400
        square_x = (screen_width - square_size) / 2
        square_y = (screen_height - square_size) / 2

        # Draw the square background
        pygame.draw.rect(screen, (0, 0, 0), (square_x,
                         square_y, square_size, square_size))

        # Create a title
        title_font = pygame.font.Font(None, 50)
        title_text = title_font.render(
            "Space Invaders 2", True, (255, 255, 255))
        title_rect = title_text.get_rect(
            center=(screen_width / 2, screen_height / 2 - 100))
        screen.blit(title_text, title_rect)

        # Controls
        title_font = pygame.font.Font(None, 25)
        title_text = title_font.render(
            "S - Shoot Laser", True, (255, 255, 255))
        title_rect = title_text.get_rect(
            center=(screen_width / 2, screen_height / 2 - 40))
        screen.blit(title_text, title_rect)

        title_font = pygame.font.Font(None, 25)
        title_text = title_font.render(
            "A/D - Rotate Left and Right", True, (255, 255, 255))
        title_rect = title_text.get_rect(
            center=(screen_width / 2, screen_height / 2 - 12))
        screen.blit(title_text, title_rect)

        title_font = pygame.font.Font(None, 25)
        title_text = title_font.render(
            "Arow Keys - Movement", True, (255, 255, 255))
        title_rect = title_text.get_rect(
            center=(screen_width / 2, screen_height / 2 + 15))
        screen.blit(title_text, title_rect)

        # Play button
        button_width, button_height = 200, 50
        button_x = (screen_width - button_width) / 2
        button_y = screen_height / 2 + 50

        # Draw the Play button
        play_button_rect = pygame.Rect(
            button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, (0, 0, 255), play_button_rect)

        # Create Play text
        play_font = pygame.font.Font(None, 40)
        play_text = play_font.render("Play", True, (255, 255, 255))
        play_text_rect = play_text.get_rect(center=play_button_rect.center)
        screen.blit(play_text, play_text_rect)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                self.game_started = True

    def gameover_screen(self):
        # Draw Game Over background
        square_size = 400
        square_x = (screen_width - square_size) / 2  # Centered on the screen
        square_y = (screen_height - square_size) / 2

        pygame.draw.rect(screen, (0, 0, 0), (square_x,
                         square_y, square_size, square_size))

        # Create a Game Over title
        title_font = pygame.font.Font(None, 50)
        title_text = title_font.render("GAME OVER", True, (255, 0, 0))
        title_rect = title_text.get_rect(
            center=(screen_width / 2, screen_height / 2 - 100))
        screen.blit(title_text, title_rect)

        # Display Score and Highscore
        if self.score > self.highscore:
            self.highscore = self.score

        score_font = pygame.font.Font(None, 30)
        score_text = score_font.render(
            f"Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(
            center=(screen_width / 2, screen_height / 2 - 60))
        screen.blit(score_text, score_rect)

        highscore_text = score_font.render(
            f"Highscore: {self.highscore}", True, (255, 255, 255))
        highscore_rect = highscore_text.get_rect(
            center=(screen_width / 2, screen_height / 2 - 40))
        screen.blit(highscore_text, highscore_rect)

        # Replay button
        button_width, button_height = 200, 50
        button_x = (screen_width - button_width) / 2
        button_y = screen_height / 2

        replay_button_rect = pygame.Rect(
            button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, (0, 255, 0), replay_button_rect)

        replay_text = pygame.font.Font(None, 40).render(
            "Replay", True, (255, 255, 255))
        replay_text_rect = replay_text.get_rect(
            center=replay_button_rect.center)
        screen.blit(replay_text, replay_text_rect)

        # Exit button
        exit_button_y = button_y + 60
        exit_button_rect = pygame.Rect(
            button_x, exit_button_y, button_width, button_height)
        pygame.draw.rect(screen, (255, 0, 0), exit_button_rect)

        exit_text = pygame.font.Font(None, 40).render(
            "Exit", True, (255, 255, 255))
        exit_text_rect = exit_text.get_rect(center=exit_button_rect.center)
        screen.blit(exit_text, exit_text_rect)

        # Handle button clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if replay_button_rect.collidepoint(event.pos):
                self.restart_game()
            elif exit_button_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    def restart_game(self):
        self.lives = 3
        self.score = 0
        self.game_started = True
        self.aliens.empty()
        self.alien_setup1(rows=2, cols=6, offset=(
            (screen_width-340)/2, 20))
        self.alien_setup2(rows=2, cols=6, offset=(
            (screen_width-340)/2, screen_height-90))
        self.alien_setup3(rows=6, cols=2, offset=(
            (10, (screen_height-340)/2,)))
        self.alien_setup4(rows=6, cols=2, offset=(
            (screen_width-100, (screen_height-340)/2,)))
        self.player.sprite.rect.center = (
            screen_width / 2, screen_height / 2)

    def restart_round(self):
        self.alien_laserSpeed = self.alien_laserSpeed + 1
        self.alien_speed = self.alien_speed + 1
        self.aliens.empty()
        self.alien_setup1(rows=2, cols=6, offset=(
            (screen_width-340)/2, 20))
        self.alien_setup2(rows=2, cols=6, offset=(
            (screen_width-340)/2, screen_height-90))
        self.alien_setup3(rows=6, cols=2, offset=(
            (10, (screen_height-340)/2,)))
        self.alien_setup4(rows=6, cols=2, offset=(
            (screen_width-100, (screen_height-340)/2,)))
        self.player.sprite.rect.center = (
            screen_width / 2, screen_height / 2)

    def run(self):
        if self.game_started:
            self.player.update()
            self.aliens.update(self.alien_direction)
            self.alien_position_checker()
            self.alien_lasers.update()
            self.player.draw(screen)
            self.player.sprite.lasers.draw(screen)
            self.aliens.draw(screen)
            self.alien_lasers.draw(screen)
            self.collision_check()
            self.display_lives()
            self.display_score()
            current_time = pygame.time.get_ticks()
            if len(self.aliens) == 0:
                self.restart_round()
            if current_time - self.alien_shoot_timer >= self.alien_shoot_interval:
                self.alien_shoot()
                self.alien_shoot()
                self.alien_shoot_timer = current_time
        elif not self.game_started and self.lives <= 0:
            self.gameover_screen()
        else:
            self.start_screen()


if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame. display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # if event.type == ALIENLASER:
            #     game.alien_shoot()
            #     game.alien_shoot()

        screen.fill((30, 30, 30))
        game.run()

        pygame.display.flip()
        clock.tick(60)
