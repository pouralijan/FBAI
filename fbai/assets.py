import pathlib
import pygame

class Assets:
    def __init__(self) -> None:
        self.width = 600
        self.height = 800

        assets_path = pathlib.Path("flappy-bird-assets")
        if not assets_path.exists:
            print("....")
        sprites_path = assets_path.joinpath("sprites")

        background_day = sprites_path.joinpath("background-day.png")
        background_night = sprites_path.joinpath("background-night.png")
        background_base = sprites_path.joinpath("base.png")

        bird_up= sprites_path.joinpath("redbird-upflap.png")
        bird_mid = sprites_path.joinpath("redbird-midflap.png")
        bird_down= sprites_path.joinpath("redbird-downflap.png")

        pipe = sprites_path.joinpath("pipe-green.png")

        background_image = pygame.image.load(background_day)
        base_image = pygame.image.load(background_base)

        self.background = pygame.transform.scale(background_image, (self.width, self.height))
        self.base = pygame.transform.scale(base_image, (self.width, 150))
        self.pipe = pygame.image.load(pipe)
        self.bird_animated = [
            pygame.image.load(bird_up),
            pygame.image.load(bird_mid),
            pygame.image.load(bird_down),
        ] 

    @property
    def bird(self):
        while True:
            for bird in self.bird_animated:
                yield bird
    


