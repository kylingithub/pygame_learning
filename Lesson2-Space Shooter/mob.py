import pygame
import random
from os import path
from env import Env

meteor_img = pygame.image.load(path.join(Env.img_dir, "meteorBrown_med1.png"))

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        size = random.randrange(3, 8)
        self.image_orig = pygame.transform.scale(meteor_img, (size * 9, size * 8))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(Env.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(5, 10)
        self.speedx = random.randrange(-3, 3)
        self.radius = int(self.rect.width * .85 / 2)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # 消失於螢幕下之後重新隨機出現在上方
        if self.rect.top > Env.HEIGHT + 10:
            self.rect.x = random.randrange(Env.WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
        self.rotate()

    def rotate(self):
        """
        update degree per 50ms
        :return: void
        """
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_img = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_img
            self.rect = self.image.get_rect()
            self.rect.center = old_center

        # do rotation here
