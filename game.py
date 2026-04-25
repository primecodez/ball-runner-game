import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Runner")

clock = pygame.time.Clock()

# ball
ball_x = 100
ball_y = 300
radius = 20
gravity = 0
on_ground = True

# obstacles
obstacles = []

# score + speed
score = 0
speed = 6
font = pygame.font.Font(None, 36)

spawn_timer = 0

def create_obstacle():
    type = random.choice(["thorn", "block"])
    
    if type == "thorn":
        # taller thorn → harder to skip
        return {"rect": pygame.Rect(800, 300, 20, 60), "type": "thorn"}
    else:
        return {"rect": pygame.Rect(800, 280, 30, 80), "type": "block"}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and on_ground:
        gravity = -12
        on_ground = False

    # physics
    gravity += 0.6
    ball_y += gravity

    if ball_y >= 300:
        ball_y = 300
        gravity = 0
        on_ground = True

    # spawn obstacles
    spawn_timer += 1
    if spawn_timer > 60:
        obstacles.append(create_obstacle())
        spawn_timer = 0

    # increase speed slowly
    speed = 6 + score // 500   # every 500 score → faster

    # move obstacles
    for obs in obstacles:
        obs["rect"].x -= speed

    # remove off-screen
    obstacles = [obs for obs in obstacles if obs["rect"].x > -50]

    # collision (more accurate)
    ball_rect = pygame.Rect(ball_x - radius, ball_y - radius, radius*2, radius*2)

    for obs in obstacles:
        if ball_rect.colliderect(obs["rect"]):
            print("Game Over! Score:", score)
            pygame.quit()
            sys.exit()

    # score
    score += 1

    # draw
    screen.fill((30, 30, 30))

    pygame.draw.circle(screen, (0, 255, 0), (ball_x, int(ball_y)), radius)

    for obs in obstacles:
        if obs["type"] == "thorn":
            pygame.draw.rect(screen, (255, 0, 0), obs["rect"])
        else:
            pygame.draw.rect(screen, (0, 0, 255), obs["rect"])

    text = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(60)