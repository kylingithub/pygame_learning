import pygame
import random

SHOT_DELAY = 300

YELLOW = (255, 255, 0)

HEIGHT = 600

WIDTH = 800

BLACK = (0, 0, 0)

GREEN = (0, 255, 0)

RED = (255, 0, 0)

FPS = 30


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        # TODO shump img
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = 8

    def update(self):
        self.keyEventHandling()

    def keyEventHandling(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            # print("move left")
            player.move(-self.speedx, 0)
        if keystate[pygame.K_RIGHT]:
            player.move(self.speedx, 0)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size = random.randrange(1, 8)
        self.image = pygame.Surface((self.size * 8, self.size * 8))
        # TODO image
        self.image.fill(RED)
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
        self.image = pygame.Surface((5, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = posx
        self.rect.centery = posy
        self.speedy = 10

    def update(self):
        self.rect.y -= self.speedy
        if self.rect.bottom < 0:
            self.kill()


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

meteors = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

last_shot = pygame.time.get_ticks()
now = 0

player = Player(WIDTH / 2, HEIGHT - 50)


def newMeteor():
    global all_sprites
    m = Meteor()
    meteors.add(m)
    all_sprites.add(m)


for i in range(8):
    newMeteor()

all_sprites.add(bullets)
all_sprites.add(player)
all_sprites.add(meteors)
running = True


def check_shoot():
    global now, last_shot, bullets, all_sprites
    keystate = pygame.key.get_pressed()
    if (keystate[pygame.K_SPACE]):
        now = pygame.time.get_ticks()
        if now - last_shot > SHOT_DELAY:
            last_shot = now
            bullet = Bullet(player.rect.centerx, player.rect.top)
            bullets.add(bullet)
            all_sprites.add(bullet)


def check_meteor_hit_player():
    global running, meteors
    hits = pygame.sprite.spritecollide(player, meteors, False, pygame.sprite.collide_rect_ratio(1))
    if hits:
        for hit in hits:
            hit.kill()
            print("check_meteor_hit_player")
            newMeteor()
            running = False


def check_bullets_hit_meteor():
    hits = pygame.sprite.groupcollide(bullets, meteors, True, True, pygame.sprite.collide_rect_ratio(1))

    if hits:
        for hit in hits:
            hit.kill()
            print("check_bullets_hit_meteor")
            newMeteor()
            # TODO explosion
            # TODO add score


while running:
    # clocks control how fast the loop will execute
    clock.tick(FPS)

    # event trigger
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         bullet = Bullet(player.rect.centerx, player.rect.centery)
        #         all_sprites.add(bullet)

    check_shoot()

    # update the state of sprites
    check_meteor_hit_player()
    #
    check_bullets_hit_meteor()

    all_sprites.update()

    # draw on screen
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # flip to display
    pygame.display.flip()

pygame.quit()
