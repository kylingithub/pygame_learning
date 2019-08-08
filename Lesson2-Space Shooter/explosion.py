import pygame
import random
from os import path
from env import Env

explosion_ani_dir = path.join(Env.img_dir, 'ani_explosion')
player_expl_ani_dir = path.join(Env.img_dir, 'ani_player_explosion')


class Explosion(pygame.sprite.Sprite):
    explosion_anim = {}
    explosion_sound = []

    explosion_anim['lg'] = []
    explosion_anim['sm'] = []
    explosion_anim['player'] = []
    for i in range(9):
        filename = 'regularExplosion0{}.png'.format(i)
        img = pygame.image.load(path.join(explosion_ani_dir, filename))
        img_lg = pygame.transform.scale(img, (75, 75))
        explosion_anim['lg'].append(img_lg)
        img_sm = pygame.transform.scale(img, (32, 32))
        explosion_anim['sm'].append(img_sm)
    for i in range(9):
        filename = 'sonicExplosion0{}.png'.format(i)
        img = pygame.image.load(path.join(player_expl_ani_dir, filename))
        explosion_anim['player'].append(img)

    if (not pygame.mixer.get_init()):
        pygame.mixer.init()
    explosion_sound.append(pygame.mixer.Sound(path.join(Env.snd_dir, "expl3.wav")))
    explosion_sound.append(pygame.mixer.Sound(path.join(Env.snd_dir, "expl6.wav")))

    def __init__(self, center, size_tag):
        pygame.sprite.Sprite.__init__(self)

        # animation and parameters of sprite

        self.size_tag = size_tag
        self.image = Explosion.explosion_anim[self.size_tag][0]
        self.rect = self.image.get_rect()
        self.rect.center = center

        # parameter
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def play(self):
        random.choice(Explosion.explosion_sound).play()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion_anim[self.size_tag]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.size_tag][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
