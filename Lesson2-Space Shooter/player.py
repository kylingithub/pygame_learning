import pygame
from os import path
from env import Env

class Player(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (50, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = Env.WIDTH / 2
        self.rect.bottom = Env.HEIGHT - 10
        self.speedx = 0
        self.radius = int(self.rect.width / 2)
        self.shield = 100
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        self.death_sound = pygame.mixer.Sound(path.join(Env.snd_dir, 'rumble1.ogg'))

    def update(self):
        self.rect.x += self.speedx
        self.speedx = 0

        if self.rect.right > Env.WIDTH:
            self.rect.right = Env.WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = Env.WIDTH / 2
            self.rect.bottom = Env.HEIGHT - 10
        # timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > 5000:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (Env.WIDTH / 2, Env.HEIGHT + 200)

    def died(self):
        self.death_sound.play()
        self.lives -= 1
        self.shield = 100

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

