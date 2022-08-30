import pygame
import random
from math import sqrt, pow
from pygame import mixer

pygame.init()

score = 0
scoreX = 10
scoreY = 10

font = pygame.font.Font('font.ttf', 32)
overfond = pygame.font.Font('font.ttf', 64)

screen = pygame.display.set_mode((800, 600))

running = True

pygame.display.set_caption(("SPACE INVADERS"))
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

background = pygame.image.load('background.png')

mixer.music.load('background.wav')
mixer.music.play(-1)

bullet = pygame.image.load('bullet.png')
bullet_x = random.randint(0, 736)
bullet_y = 480
bullet_change = 0
state = True

playerIma = pygame.image.load('player.png')
player_x = 370
player_y = 480
player_change = 0

enemyIma = []
enemy_x = []
enemy_y = []
enemyX_change = []
enemyY_change = []
count = 6
for i in range(6):
    enemyIma.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(0)
    enemyX_change.append(pow(-1, i) * 4)
    enemyY_change.append(30)


def printscore(x, y):
    Pscore = font.render("SCORE : " + str(score), True, (255, 255, 255))
    screen.blit(Pscore, (x, y))


def overgame():
    over = overfond.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (150, 200))


def player(x, y):
    screen.blit(playerIma, (x, y))


def enemy(x, y, i):
    screen.blit(enemyIma[i], (x, y))


def firebullet(x, y):
    global state
    screen.blit(bullet, (x + 16, y))


def distance(enemyX, enemyY, bulletX, bulletY):
    dis = sqrt(pow((enemyX - bulletX), 2) + pow((enemyY - bulletY), 2))
    if dis < 27:
        return True
    else:
        return False


overgame()

while running:

    screen.fill((155, 155, 100))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_change = -5
            if event.key == pygame.K_RIGHT:
                player_change = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_change = 0

    if (player_x < 0):
        player_x = 0
    if (player_x > 736):
        player_x = 736
    player_x += player_change
    player(player_x, player_y)

    if state == True:
        bullet_x = player_x
        state = False
        shoot = mixer.Sound('laser.wav')
        shoot.play()
    firebullet(bullet_x, bullet_y)
    bullet_y -= 10
    if (bullet_y < 0):
        bullet_y = 480
        state = True
    for i in range(6):

        dis = distance(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if (dis):
            state = True
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = 0
            score += 1
            dis = mixer.Sound('explosion.wav')
            dis.play()

        if (enemy_x[i] <= 0):
            enemyX_change[i] = 4
            enemy_y += enemyY_change

        if (enemy_x[i] >= 736):
            enemyX_change[i] = -4
            enemy_y[i] += enemyY_change[i]

        enemy_x[i] += enemyX_change[i]
        enemy(enemy_x[i], enemy_y[i], i)
        printscore(scoreX, scoreY)

        if (enemy_y[i]>100) :
            for j in range(6):
                enemy_y[j]=2000
            overgame()
    pygame.display.update()
