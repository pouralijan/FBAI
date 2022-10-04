import pygame
from world import Background, World
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
        self.background = pygame.sprite.GroupSingle(Background())
        self.world = World(score_signal=self.score_signal)
        self.score = 0

        self.font = pygame.font.SysFont("comicsans", 32)
        self.score_label = self.font.render("Score: " + str(self.score),1,(255,255,255))

    def __del__(self):
        pygame.quit()

    def score_signal(self):
        self.score += 1
        self.score_label = self.font.render("Score: " + str(self.score),1,(255,255,255))

    def chech_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == self.screen_update:
                self.background.draw(self.screen)
                self.world.update()
                self.world.draw(self.screen)
                self.player.update()
                self.player.draw(self.screen)
                self.screen.blit(self.score_label, (self.width - self.score_label.get_width() - 15, 10))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    for player in self.player.sprites():
                        player.jump()

    def check_collision(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.world, False):
            print("Game Over ...")
            return True
        return False
    def run(self):
        while self.is_running:
            self.chech_event()
            self.is_running = not self.check_collision()
            pygame.display.update()
            self.clock.tick(30)
