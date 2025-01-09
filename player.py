import pygame
import math
from laser import Laser


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, size, constraintx, constrainty, speed):
        super().__init__()
        self.original_image = pygame.image.load(
            '../SpaceInvaders/graphics/player.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, size)
        self.image = self.original_image
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed
        self.max_x_constraint = constraintx
        self.max_x = constraintx
        self.max_y_constraint = constrainty-62
        self.rotation_angle = 0
        self.ready = True
        self.rotate_right = True
        self.rotate_left = True
        self.laser_time = 0
        self.laser_cooldown = 600
        self.lasers = pygame.sprite.Group()
        self.rotation = 0

    def get_input(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_RIGHT]:
            dx += 1
        if keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_DOWN]:
            dy += 1

        # Normalize the vector if there's any movement
        if dx != 0 or dy != 0:
            # Calculate the magnitude of the vector
            length = math.sqrt(dx**2 + dy**2)

            # Normalize the vector by dividing by its magnitude
            dx /= length
            dy /= length

            # Move the player by the normalized vector scaled by speed
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

        if keys[pygame.K_s] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
        if keys[pygame.K_a] and self.rotate_right:
            self.rotation_angle += 90
            self.rotate_right = False
            if self.rotation_angle == 360:
                self.rotation_angle = 0
        elif keys[pygame.K_d] and self.rotate_left:
            self.rotation_angle -= 90
            self.rotate_left = False
            if self.rotation_angle == -90:
                self.rotation_angle = 270
        if not keys[pygame.K_a]:
            self.rotate_right = True
        if not keys[pygame.K_d]:
            self.rotate_left = True

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint
        if self.rect.y >= self.max_y_constraint:
            self.rect.y = self.max_y_constraint
        if self.rect.y <= 0:
            self.rect.y = 0

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, -8, 'blue',
                        self.max_y_constraint, self.max_x, self.rotation_angle))

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def rotate(self):
        self.image = pygame.transform.rotate(
            self.original_image, self.rotation_angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.get_input()
        self.rotate()
        self.constraint()
        self.recharge()
        self.lasers.update()
