import pygame
from world import World
from bird import Bird

import yaml

class Game:
    def __init__(self) -> None:
        with open ('fbai/config.yaml') as config_file:
            config = yaml.load(config_file, Loader=yaml.Loader)

        pygame.init()
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.screen_update = pygame.USEREVENT
        pygame.time.set_timer(self.screen_update, 30)
        self.width = config.get("game").get("display").get("width")
        self.height = config.get("game").get("display").get("hight")


        self.screen = pygame.display.set_mode((self.width, self.height))
        self.player = pygame.sprite.GroupSingle(Bird())
        self.world = World()

    def __del__(self):
        pygame.quit()

    def chech_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == self.screen_update:
                self.world.update()
                self.world.draw(self.screen)
                self.player.update()
                self.player.draw(self.screen)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    for player in self.player.sprites():
                        player.jump()

    def run(self):
        while self.is_running:
            self.chech_event()
            pygame.display.update()
            self.clock.tick(30)
