import pygame
import random
from env import Env
from os import path

powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(Env.img_dir, 'shield_gold.png'))
powerup_images['gun'] = pygame.image.load(path.join(Env.img_dir, 'bolt_gold.png'))

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the bottom of the screen
        if self.rect.top > Env.HEIGHT:
            self.kill()

    def play(self):
        # TODO sound
        pass
