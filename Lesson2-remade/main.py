import random
from os import path

import pygame

# TODO Refactor 將參數統一放到另外一個檔案
SHOT_DELAY = 300

YELLOW = (255, 255, 0)

HEIGHT = 600

WIDTH = 800

BLACK = (0, 0, 0)

GREEN = (0, 255, 0)

RED = (255, 0, 0)

FPS = 30

img_dir = path.join(path.dirname(__file__), 'img')
sound_dir = path.join(path.dirname(__file__), 'sound')
font_name = pygame.font.match_font('arial')
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(path.join(sound_dir, "bgm.mp3"))
pygame.mixer.music.play(-1)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load(path.join(img_dir, "ship.png"))
        self.image = pygame.transform.scale(image, (50, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = 8

    def update(self):
        self.keyEventHandling()

    def keyEventHandling(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            player.move(-self.speedx, 0)
        if keystate[pygame.K_RIGHT]:
            player.move(self.speedx, 0)
        # TODO 01.新增上下移動
        # TODO 01.讓船不會飛出場外

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size = random.randrange(3, 8)
        image = pygame.image.load(path.join(img_dir, "meteor.png"))
        self.image = pygame.transform.scale(image, (self.size * 8, self.size * 8))

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH)
        self.rect.y = 0
        self.speedx = random.randint(-5, 5)
        self.speedy = random.randint(7, 15)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.y > HEIGHT):
            newMeteor()
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(path.join(img_dir, "laser_gun.png"))
        self.rect = self.image.get_rect()
        self.rect.centerx = posx
        self.rect.centery = posy
        self.speedy = 10

    def update(self):
        self.rect.y -= self.speedy
        if self.rect.bottom < 0:
            self.kill()


def newMeteor():
    global all_sprites
    m = Meteor()
    meteors.add(m)
    all_sprites.add(m)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.image.load(path.join(img_dir, 'background.png'))
bg_rect = bg.get_rect()
clock = pygame.time.Clock()

meteors = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

last_shot = pygame.time.get_ticks()
now = 0
score = 0
player = Player(WIDTH / 2, HEIGHT - 50)

for i in range(8):
    newMeteor()

all_sprites.add(bullets)
all_sprites.add(player)
all_sprites.add(meteors)
running = True
sound_pew = pygame.mixer.Sound(path.join(sound_dir, "pew.wav"))


def check_meteor_hit_player():
    global running, meteors
    # TODO 05.修正碰撞偵測的規則
    hits = pygame.sprite.spritecollide(player, meteors, False)
    if hits:
        for hit in hits:
            hit.kill()
            # print("check_meteor_hit_player")
            newMeteor()
            # TODO 07.修改死亡的規則，改成扣血扣到0時，遊戲才結束
            running = False


def check_bullets_hit_meteor():
    global score
    # TODO 05.修正碰撞偵測的規則
    hits = pygame.sprite.groupcollide(bullets, meteors, True, True)
    if hits:
        for hit in hits:
            hit.kill()
            # TODO 02.修改加分的機制
            score += 1
            # print("check_bullets_hit_meteor")
            newMeteor()
            # TODO 04.增加爆炸的動畫
            # TODO 06.擊破隕石會掉出武器或是能量包 武器可以改變攻擊模式 能量包可以回血


def draw_score():
    font = pygame.font.Font(font_name, 14)
    text_surface = font.render(str(score), True, YELLOW)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (WIDTH / 2, 20)
    screen.blit(text_surface, text_rect)
    pass


def shoot():
    sound_pew.play()
    bullet = Bullet(player.rect.centerx, player.rect.centery)
    bullets.add(bullet)
    all_sprites.add(bullet)


while running:
    # clocks control how fast the loop will execute
    clock.tick(FPS)

    # event trigger
    # TODO 08.新增起始畫面 按下空白鍵才開始遊戲
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # TODO 03.修正成子彈可以連發
            if event.key == pygame.K_SPACE:
                shoot()

    # update the state of sprites
    check_meteor_hit_player()
    #
    check_bullets_hit_meteor()

    all_sprites.update()

    # draw on screen

    # screen.fill(BLACK)
    draw_score()
    screen.blit(bg, bg_rect)
    all_sprites.draw(screen)
    # flip to display
    pygame.display.flip()

pygame.quit()
