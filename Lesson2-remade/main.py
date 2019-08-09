import pygame

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
        self.rect.centerx = x/2
        self.rect.bottom = y
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


pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

player = Player(750, 300)
all_sprites.add(player)

running = True
while running:
    # clocks control how fast the loop will execute
    clock.tick(FPS)

    # event trigger
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update the state of sprites

    all_sprites.update()

    # draw on screen
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # flip to display
    pygame.display.flip()

pygame.quit()
