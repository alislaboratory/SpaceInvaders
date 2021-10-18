import pygame
import os
pygame.font.init()
pygame.mixer.init()

# consts
WIDTH, HEIGHT = 900, 500
BG_COLOR = (40, 200, 40)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # create a window
FPS = 60
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
MAX_HEALTH = 30
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 5
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/laser_hit.wav')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/laser_fire.wav')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

pygame.display.set_caption("My First Game")

SHIP_SIZE = (55, 40)

YELLOW_SHIP = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SHIP =  pygame.transform.rotate(pygame.transform.scale(YELLOW_SHIP, SHIP_SIZE), 90)

RED_SHIP = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
RED_SHIP = pygame.transform.rotate(pygame.transform.scale(RED_SHIP, SHIP_SIZE), 270)

SPACE = pygame.image.load(os.path.join('Assets', 'space.png'))
SPACE = pygame.transform.scale(SPACE, (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # WIN.fill(BG_COLOR) uncomment this line in case of no bg
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(YELLOW_SHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SHIP, (red.x, red.y))

    red_health_text = HEALTH_FONT.render(f"Health: {str(red_health)}", 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(f"Health: {str(yellow_health)}", 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    for yellow_bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, yellow_bullet)

    for red_bullet in red_bullets:
        pygame.draw.rect(WIN, RED, red_bullet)


    pygame.display.update()


def yellow_movement_handler(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL + 10 > 0:  # left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width - 20 < BORDER.x:  # right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL + 5 > 0:  # up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height + 10 < HEIGHT:  # down
        yellow.y += VEL


def bullet_handler(yellow_bullets, red_bullets, yellow, red):

    for yellow_bullet in yellow_bullets:
        yellow_bullet.x += BULLET_VEL

        if red.colliderect(yellow_bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(yellow_bullet)

        elif yellow_bullet.x > WIDTH:
            yellow_bullets.remove(yellow_bullet)

    for red_bullet in red_bullets:
        red_bullet.x -= BULLET_VEL

        if yellow.colliderect(red_bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(red_bullet)

def red_movement_handler(keys_pressed, red):
    if keys_pressed[pygame.K_j] and red.x - VEL - 5 > BORDER.x:  # left
        red.x -= VEL
    if keys_pressed[pygame.K_l] and red.x + VEL + red.width - 30 < WIDTH:  # right
        red.x += VEL
    if keys_pressed[pygame.K_i] and red.y - VEL + 5 > 0:  # up
        red.y -= VEL
    if keys_pressed[pygame.K_k] and red.y + VEL + red.height + 10 < HEIGHT:  # down
        red.y += VEL

def winner_screen(winner_text):
    text = WINNER_FONT.render(winner_text, 1, WHITE)
    WIN.blit(text, (WIDTH/2  - text.get_width()/2, HEIGHT/2))
    pygame.display.update()
    pygame.time.delay(5000)
    pygame.quit()


def main():  # the main pygame loop
    red = pygame.Rect(700, 300, SHIP_SIZE[0], SHIP_SIZE[1])
    yellow = pygame.Rect(100, 300, SHIP_SIZE[0], SHIP_SIZE[1])
    red_bullets = []
    yellow_bullets = []
    red_health = MAX_HEALTH
    yellow_health = MAX_HEALTH
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == RED_HIT:
                red_health -= 10
                BULLET_HIT_SOUND.play()


            if event.type == YELLOW_HIT:
                yellow_health -= 10
                BULLET_HIT_SOUND.play()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 4)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 4)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

        winner_text = ""

        if red_health <= 0:
            winner_text = "Yellow Won!"

        if yellow_health <= 0:
            winner_text = "Red Won!"


        if winner_text != "":
            winner_screen(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_movement_handler(keys_pressed, yellow)
        red_movement_handler(keys_pressed, red)
        bullet_handler(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()


if __name__ == "__main__":
    main()



