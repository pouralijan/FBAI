from time import sleep
import pygame
import random
from typing import Any, List, Sequence, Union
from pygame.sprite import AbstractGroup, Sprite


from assets import Assets

class PipeSprint(pygame.sprite.Sprite):
    def __init__(self, offset : pygame.sprite.Sprite = None, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        assets = Assets()

        self.image = assets.pipe
        self.speed = 3
        if offset:
            self.image = self.image.subsurface((0, 0, self.image.get_width(),800 - (offset.image.get_height() + 100 + 150 )))
            self.rect = self.image.get_rect()
            print(f"Offset.rect: {offset.rect}")
            print(f"self.rect: {self.rect}")
            self.rect.x = offset.rect.x
            self.rect.y = offset.rect.height + 100
        else:
            self.image = self.image.subsurface((0, 0, self.image.get_width(), random.randint(self.image.get_height()-50, self.image.get_height())))
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect()
            self.rect.y = 0
            print(self.rect)
        self.rect.x = 600

    def update(self):
        if self.rect.x < self.image.get_width() * -2:
            self.kill()
        self.rect.x -= self.speed

class Pipe(pygame.sprite.Group):
    def __init__(self, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        super().__init__(*sprites)
        up = PipeSprint()
        down = PipeSprint(up)
        self.add([up, down])
        
class Background(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.assets = Assets()
        self.image = self.assets.background
        self.rect = self.image.get_rect()

class Base(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.assets = Assets()
        self.image = self.assets.base
        center = (600 / 2, 800 - (self.assets.base.get_height()/2))
        self.rect = self.image.get_rect(center=center)
        print(self.rect)
        
class World(pygame.sprite.Group):
    def __init__(self, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        super().__init__(*sprites)
        self.add([Background(), Base(), Pipe()])

    def update(self):
        last_sprite = self.sprites()[-1]
        if hasattr(last_sprite, "rect") and last_sprite.rect.x < 400:
            self.add([Pipe()])
        
        for sprite in self.sprites():
            sprite.update()
        