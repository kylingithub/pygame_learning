from os import path
import pygame

class Env:
    WIDTH = 480  # width of our game window
    HEIGHT = 600  # height of our game window
    FPS = 60  # frames per second
    img_dir = path.join(path.dirname(__file__), 'img')
    snd_dir = path.join(path.dirname(__file__), 'sound')
    shoot_delay = 250
    player_img = pygame.image.load(path.join(img_dir, "playerShip3_orange.png"))
    player_mini_img = pygame.transform.scale(player_img, (25, 19))
    background = pygame.image.load(path.join(img_dir, 'starfield.png'))
    background_rect = background.get_rect()

    @staticmethod
    def bgm_play():
        pygame.mixer.music.load(path.join(Env.snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.mp3'))
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)


# Colors (R, G, B)
class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
