import pygame

RED = (255, 0, 0)

FPS = 30

pygame.init()
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()


running = True
while running:
    # clocks control how fast the loop will execute
    clock.tick(FPS)

    # event trigger
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running = False

    # update the state of sprites
    all_sprites.update()

    # draw on screen
    screen.fill(RED)

    # flip to display
    pygame.display.flip()


pygame.quit()