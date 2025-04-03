import pygame
from pygame.locals import *
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# load sounds
BULLET_HIT_SOUND = pygame.mixer.Sound('Lesson_6/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Lesson_6/Gun+Silencer.mp3')

#load fonts
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

#decide frame rate/ velocity etc
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# loading spaceship images
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Lesson_6', 'spaceship_yellow.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Lesson_6', 'spaceship_red.png'))

#transforming and scaling to match the window size
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Lesson_6', 'space.png')), (WIDTH, HEIGHT))

#create a border
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# intialize health
red_health=10
yellow_health=10

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, image, angle, x, y):
        super().__init__()
        self.image=pygame.transform.rotate(pygame.transform.scale(image, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), angle)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    
    def movehorizontal(self, v, player):
        self.rect.x+=v
        if player==1:
            if self.rect.left<=0 or self.rect.right>=BORDER.left:
                self.rect.move_ip(-v, 0)
        
        if player==2:
            if self.rect.left<=BORDER.right or self.rect.right>=WIDTH:
                self.rect.move_ip(-v, 0)

    def movevertical(self, v):
        self.rect.move_ip(0, v)
        if self.rect.top<=0 or self.rect.bottom>=HEIGHT:
            self.rect.move_ip(0, -v)


red=Spaceship(RED_SPACESHIP_IMAGE, 270, 670,220)
yellow=Spaceship(YELLOW_SPACESHIP_IMAGE, 90, 220,220)
sprites=pygame.sprite.Group()
sprites.add(red)
sprites.add(yellow)

def draw_window():
        WIN.blit(SPACE, (0, 0))
        pygame.draw.rect(WIN, BLACK, BORDER)
        red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
        yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
        WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
        WIN.blit(yellow_health_text, (10, 10))

def draw_bullets():
        for bullet in red_bullets:
            pygame.draw.rect(WIN, RED, bullet)
            bullet.x -= BULLET_VEL
            

        for bullet in yellow_bullets:
            pygame.draw.rect(WIN, YELLOW, bullet)
            bullet.x += BULLET_VEL
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


def handle_bullets():
    global red_health
    for bullet in yellow_bullets:
        
        if red.rect.colliderect(bullet):
            red_health -= 1
            #pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
        

    for bullet in red_bullets:
        
        if yellow.rect.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

    for bullet1 in red_bullets:
        for bullet2 in yellow_bullets:
            if bullet1.colliderect(bullet2):
                red_bullets.remove(bullet1)
                yellow_bullets.remove(bullet2)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


red_bullets = []
yellow_bullets = []

clock = pygame.time.Clock()

run = True
while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            """
            if event.type == KEYDOWN:
                if event.key==K_UP:
                    red.moveup()
                if event.key==K_DOWN:
                    red.movedown()
                if event.key==K_RIGHT:
                    red.moveright()
                if event.key==K_LEFT:
                    red.moveleft()
            """

            if event.type == KEYDOWN:
                if event.key == K_LCTRL:
                    bullet = pygame.Rect(yellow.rect.x + yellow.rect.width, yellow.rect.y + yellow.rect.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

                    BULLET_FIRE_SOUND.play()

                if event.key == K_RCTRL:
                    bullet = pygame.Rect(red.rect.x, red.rect.y + red.rect.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)

                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()


        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_a]:  # LEFT
            yellow.movehorizontal(-VEL,1)
        if keys_pressed[K_d]:  # RIGHT
            yellow.movehorizontal(VEL,1)
        if keys_pressed[K_w]:
            yellow.movevertical(-VEL) 
        if keys_pressed[K_s]:
            yellow.movevertical(VEL)
        if keys_pressed[K_LEFT]:  # LEFT
            red.movehorizontal(-VEL,2)
        if keys_pressed[K_RIGHT]:  # RIGHT
            red.movehorizontal(VEL,2)
        if keys_pressed[K_UP]: 
            red.movevertical(-VEL)
        if keys_pressed[K_DOWN]:
            red.movevertical(VEL)

        draw_window()
        sprites.draw(WIN)
        draw_bullets()
        handle_bullets()

        if red_health <= 0:
            winner_text = "Yellow Wins!"
            draw_winner(winner_text)
            run=False

        if yellow_health <= 0:
            winner_text = "Red Wins!"
            draw_winner(winner_text)
            run=False

        pygame.display.update()

pygame.quit()