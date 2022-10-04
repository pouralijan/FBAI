import random
from assets import Assets
import pygame
from pygame.sprite import AbstractGroup


class Bird(pygame.sprite.Sprite):
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.assets = Assets()
        self.bird = self.assets.bird
        self.image = next(self.bird)

        x = 250
        y = random.randint(200, 600)

        self.rect = self.image.get_rect(center=(x, y))

        self.gravity = 5
        self.tick_count = 0
        self.height = y
        self.tilt = 0

    def update(self):
        self.image = next(self.bird)
        self.tick_count += 1
        displacement = self.gravity * self.tick_count + 0.5 * 3 * (self.tick_count ** 2)
        if displacement >= 4:
            displacement = (displacement/abs(displacement)) * 4
        elif displacement < 0:
            displacement += self.gravity
        # self.rect.x = 250
        self.rect.y += displacement

    def jump(self):
        self.gravity = -6
        self.tick_count = 0
        self.height = self.rect.y
