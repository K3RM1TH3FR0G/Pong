import pygame, os
from sys import exit
from random import randint

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'#Called before pygame.init() to center the window
info = pygame.display.Info()#Called before set_mode to use the current monitor resolution
screenW = info.current_w
screenH = info.current_h
#Set the screen size and title as well as made the screen fullscreen. 
screen = pygame.display.set_mode((screenW, screenH), pygame.FULLSCREEN)
pygame.display.set_caption("PONG")
clock = pygame.time.Clock()

round_over = True

bg_color = (50, 60, 80)
font_color = (40, 50, 70)
paddle_size_x = 20
paddle_size_y = 125

paddle_start_y = (screenH/2) - (paddle_size_y/2)

paddle1 = pygame.Surface((paddle_size_x, paddle_size_y))
paddle1.fill('White')
paddle1_x = 50

paddle2 = pygame.Surface((paddle_size_x, paddle_size_y))
paddle2.fill('White')
paddle2_x = screenW - 50 - paddle_size_x

paddle1_location = paddle_start_y
paddle2_location = paddle_start_y

#Ball
ball = pygame.Surface((20, 20))
ball.fill('White')
ball_width, ball_height = ball.get_size()
ball_x = (screenW / 2) - (ball_width / 2)
ball_y = (screenH / 2) - (ball_height / 2)

def ballstart():
    global ball_speed_x, ball_speed_y, ball_speed_randomx, ball_speed_randomy
    ball_speed_randomx = randint(0, 1)
    ball_speed_randomy = randint(0, 1)
    if ball_speed_randomx == 0:
        ball_speed_x = -5
    else:
        ball_speed_x = 5
    if ball_speed_randomy == 0:
        ball_speed_y = -5
    else:
        ball_speed_y = 5
    
    return ball_speed_x, ball_speed_y

ball_speed_x, ball_speed_y = ballstart()

#Score
score1 = 0
score2 = 0
font = pygame.font.Font(None, screenH//2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    

    keys = pygame.key.get_pressed()
    #Closes the game with the escape key. 
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        exit()

    #Left Paddle
    if keys[pygame.K_w]:
        paddle1_location -= 5
    if keys[pygame.K_s]:
        paddle1_location += 5
    #Right Paddle
    if keys[pygame.K_i]:
        paddle2_location -= 5
    if keys[pygame.K_k]:
        paddle2_location += 5

    #Ball Movement
    if round_over:
        ball_speed_x = 0
        ball_speed_y = 0
        if keys[pygame.K_SPACE]:
            ball_speed_x, ball_speed_y = ballstart()
            round_over = False
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Check for collision with the left and right of the screen
    if ball_x + ball_width >= screenW:
        score1 += 1
        ball_x = (screenW / 2) - (ball_width / 2)
        ball_y = (screenH / 2) - (ball_height / 2)
        ball_speed_x = 0
        ball_speed_y = 0
        round_over = True
    elif ball_x <= 0:
        score2 += 1
        ball_x = (screenW / 2) - (ball_width / 2)
        ball_y = (screenH / 2) - (ball_height / 2)
        ball_speed_x = 0
        ball_speed_y = 0
        round_over = True

    # Check for collision with the top and bottom of the screen
    if ball_y + ball_height >= screenH or ball_y <= 0:
        ball_speed_y *= -1
    
    #Check paddle collision with top and bottom of the screen
    if paddle1_location <= 0:
        paddle1_location = 0
    elif paddle1_location >= screenH - paddle_size_y:
        paddle1_location = screenH - paddle_size_y
    if paddle2_location <= 0:
        paddle2_location = 0
    elif paddle2_location >= screenH - paddle_size_y:
        paddle2_location = screenH - paddle_size_y

    # Check for collision with paddles
    if ball_x <= paddle1_x + paddle_size_x and paddle1_x + paddle_size_x <= ball_x and paddle1_location <= ball_y + ball_height and ball_y <= paddle1_location + paddle_size_y:
        ball_speed_x *= -1
    if ball_x + paddle_size_x >= paddle2_x and ball_x + paddle_size_x<= paddle2_x and paddle2_location <= ball_y + ball_height and ball_y <= paddle2_location + paddle_size_y:
        ball_speed_x *= -1

    screen.fill(bg_color)

    #Score
    score_text = font.render(f"{score1}    {score2}", True, font_color)
    screen.blit(score_text, (screenW / 2 - score_text.get_width() / 2, screenH / 2 - score_text.get_height() / 2))

    #Paddles
    screen.blit(paddle1, (50, paddle1_location))
    screen.blit(paddle2, (screenW - 70, paddle2_location))
    screen.blit(ball, (ball_x, ball_y))

    pygame.display.update()
    clock.tick(60)
