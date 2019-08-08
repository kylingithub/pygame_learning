import pygame
import random
from env import Env
from env import Color
from mob import Mob
from explosion import Explosion
from pow import Pow
from bullets import Bullet
from player import Player

# Load all game graphics


font_name = pygame.font.match_font('arial')

pygame.init()
pygame.mixer.init()  # for sound
screen = pygame.display.set_mode((Env.WIDTH, Env.HEIGHT))
pygame.display.set_caption("Space Adventure")
clock = pygame.time.Clock()
lastShoot = pygame.time.get_ticks()
running = True
game_over = True

# Load all game sound and bgm
Env.bgm_play()

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, Color.YELLOW)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def new_mob():
    global m
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def drwa_shieldBar(surf, shield):
    outline_rect = pygame.Rect(10, 20, 200, 20)
    fill_rect = pygame.Rect(10, 20, 200 * shield / 100, 20)
    pygame.draw.rect(surf, Color.GREEN, fill_rect)
    pygame.draw.rect(surf, Color.WHITE, outline_rect, 2)


def show_go_screen():
    screen.blit(Env.background, Env.background_rect)
    draw_text(screen, "SHMUP!", 64, Env.WIDTH / 2, Env.HEIGHT / 4)
    draw_text(screen, "Arrow keys move, Space to fire", 22,
              Env.WIDTH / 2, Env.HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, Env.WIDTH / 2, Env.HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(Env.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


def shoot(rect, power):
    global lastShoot, all_sprites
    now = pygame.time.get_ticks()
    if now - lastShoot > Env.shoot_delay:
        lastShoot = now
        Bullet.play()
        if power == 1:
            bullet = Bullet(rect.centerx, rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

        if power >= 2:
            bullet1 = Bullet(rect.left, rect.centery)
            bullet2 = Bullet(rect.right, rect.centery)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            bullets.add(bullet1)
            bullets.add(bullet2)



def checkPlayHitPow():
    global hits, hit
    # check to see if player hit a powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        hit.play()
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()


def checkBulletHitMob():
    global hits, hit, expl, score

    # check if mobs are shot by bullets and generated new mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True, pygame.sprite.collide_rect_ratio(0.6))
    for hit in hits:
        new_mob()
        expl = Explosion(hit.rect.center, 'lg')
        expl.play()
        all_sprites.add(expl)
        score += hit.radius
        if random.random() > 0.5:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)


def checkPlayerHitMob():
    global hits, hit, expl, death_explosion, game_over
    # check if objects are collided
    # hits = pygame.sprite.collide_rect_ratio(0.7)
    # hits = pygame.sprite.spritecollide(player, mobs, False)
    # hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle_ratio(1))
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    if hits:
        for hit in hits:
            player.shield -= hit.radius
            print(player.shield)
            new_mob()
            expl = Explosion(hit.rect.center, 'sm')
            expl.play()
            all_sprites.add(expl)
            if player.shield <= 0:
                death_explosion = Explosion(player.rect.center, 'player')
                all_sprites.add(death_explosion)
                player.died()
                player.hide()

    if player.lives == 0 and not death_explosion.alive():
        game_over = True


def game_reset():
    global game_over, all_sprites, mobs, bullets, powerups, player, score
    game_over = False
    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    player = Player(Env.player_img)
    all_sprites.add(player)
    for i in range(8):
        new_mob()
    score = 0


# Game Loop


game_reset()

while running:
    # keep loop running at the right speed
    clock.tick(Env.FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_LEFT]:
        player.speedx = -8
    if keystate[pygame.K_RIGHT]:
        player.speedx = 8
    if keystate[pygame.K_SPACE]:
        shoot(player.rect, player.power)

    if game_over:
        show_go_screen()
        game_reset()

    checkPlayerHitMob()
    checkBulletHitMob()
    checkPlayHitPow()

    # Update
    all_sprites.update()

    # Draw / render

    screen.fill(Color.BLACK)
    screen.blit(Env.background, Env.background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 24, Env.WIDTH / 2, 10)
    drwa_shieldBar(screen, player.shield)

    draw_lives(screen, Env.WIDTH - 100, 5, player.lives,
               Env.player_mini_img)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
