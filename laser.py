import pygame


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, color, constrainty, constraintx, rotation):
        super().__init__()
        self.image = pygame.Surface((4, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.y_constraint = constrainty
        self.x_constraint = constraintx
        self.rotation_angle = rotation

        self.image = pygame.transform.rotate(self.image, -self.rotation_angle)
        self.rect = self.image.get_rect(center=pos)

    def destory(self):
        if self.rect.y <= -50 or self.rect.y >= self.y_constraint + 50 or self.rect.x <= -50 or self.rect.x >= self.x_constraint + 50:
            self.kill()

    def update(self):
        if self.rotation_angle == 0:
            self.rect.y += self.speed
            self.destory()
        if self.rotation_angle == 180:
            self.rect.y -= self.speed
            self.destory()
        if self.rotation_angle == 90:
            self.rect.x += self.speed
            self.destory()
        if self.rotation_angle == 270:
            self.rect.x -= self.speed
            self.destory()
