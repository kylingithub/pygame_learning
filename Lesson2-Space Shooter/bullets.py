import pygame
from os import path
from env import Env

bullet_img = pygame.image.load(path.join(Env.img_dir, "laserRed07.png"))
shoot_sound = pygame.mixer.Sound(path.join(Env.snd_dir, "pew.wav"))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

    @staticmethod
    def play():
        shoot_sound.play()