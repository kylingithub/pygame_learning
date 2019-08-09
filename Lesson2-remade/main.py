import pygame
import random

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
            all_sprites.add(Meteor())
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 20))
        self.image.fill((255, 255, 0))
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

player = Player(WIDTH / 2, HEIGHT - 50)
for i in range(8):
    meteors.add(Meteor())

all_sprites.add(player)
all_sprites.add(meteors)
running = True
while running:
    # clocks control how fast the loop will execute
    clock.tick(FPS)

    # event trigger
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.centery)
                all_sprites.add(bullet)
    # keystate = pygame.key.get_pressed()
    # if(keystate[pygame.K_SPACE]):
    #     bullet = Bullet(player.rect.centerx,player.rect.centery)
    #     all_sprites.add(bullet)
    # update the state of sprites

    all_sprites.update()

    # draw on screen
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # flip to display
    pygame.display.flip()

pygame.quit()
