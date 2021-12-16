import pygame
import random
import math
from pygame import mixer

#------------------------------#

# initialize the pygame
pygame.init()  

# create the screen
screen = pygame.display.set_mode((800,600)) 

# Background
backgroung = pygame.image.load('bg.png')

# Background Sound
mixer.music.load('background.wav')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption('Space Invader by B1ackmonday')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Bullet

# Ready - Can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 4
bulletY_change = 8
bullet_state = 'ready'

# Font
score_value = 0
font = pygame.font.Font('poxel-font.ttf',30)

textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('poxel-font.ttf',80)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render('Score :' + str(score_value),True, (0,255,0))
    screen.blit(score,(x,y))

def game_over_text():
    over_font = font.render('GAME OVER',True, (255,255,51))
    screen.blit(over_font,(320,250))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg,(x+16, y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    # Formula - Distance between two points and the midpoint
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:

    # RGB : Red, Green, Blue
    screen.fill((0,0,0))
    # Background Image
    screen.blit(backgroung,(0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right/left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.set_volume(0.8)
                    bullet_Sound.play()
                    # Get the current x cordinate of the player
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    # Checking for boundaries of spaceship so it doesn't go out of bounds
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # from edge 800 - 64(player Image size) 
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:  
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision: 
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.set_volume(0.8)
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 10
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
        
        enemy(enemyX[i],enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

   

    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()

    
