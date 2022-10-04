from time import sleep
import pygame
import random
from typing import Sequence, Union
from pygame.sprite import AbstractGroup, Sprite


from assets import Assets

class PipeSprint(pygame.sprite.Sprite):
    def __init__(self, offset : pygame.sprite.Sprite = None, score_signal = None, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        assets = Assets()
        self.score_signal = score_signal
        self.signal_sent = False

        self.image = assets.pipe
        self.speed = 3
        if offset:
            self.image = self.image.subsurface((0, 0, self.image.get_width(),800 - (offset.image.get_height() + 100 + 150 )))
            self.rect = self.image.get_rect()
            self.rect.x = offset.rect.x
            self.rect.y = offset.rect.height + 100
        else:
            self.image = self.image.subsurface((0, 0, self.image.get_width(), random.randint(self.image.get_height()-50, self.image.get_height())))
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect()
            self.rect.y = 0
        self.rect.x = 600

    def update(self):
        if self.rect.x < 200 and not self.signal_sent:
            if self.score_signal:
                self.score_signal()
                self.signal_sent = True
        if self.rect.x < self.image.get_width() * -2:
            self.kill()
        self.rect.x -= self.speed

class Pipe(pygame.sprite.Group):
    def __init__(self, score_signal, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        super().__init__(*sprites)
        self.score_signal = score_signal
        up = PipeSprint(score_signal = score_signal)
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
        
class World(pygame.sprite.Group):
    def __init__(self, score_signal =None,*sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        super().__init__(*sprites)
        self.score_signal = score_signal
        self.add([Base(), Pipe(self.score_signal)])

    def update(self):
        last_sprite = self.sprites()[-1]
        if hasattr(last_sprite, "rect") and last_sprite.rect.x < 400:
            self.add([Pipe(self.score_signal)])
        
        for sprite in self.sprites():
            sprite.update()
        