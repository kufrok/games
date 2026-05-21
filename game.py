import pygame
import sys
import random

pygame.init()

# Okno
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# Barvy
BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)
GREEN = (0, 200, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Pták
bird_x = 100
bird_y = 300
bird_radius = 20
bird_velocity = 0
gravity = 0.25   # pomalejší pád
jump_strength = -7  # menší skok

# Trubky
pipe_width = 60
pipe_gap = 200
pipe_velocity = 3
pipes = []

# Skóre
score = 0
game_active = True


def reset_game():
    global bird_y, bird_velocity, pipes, score, game_active
    bird_y = 300
    bird_velocity = 0
    pipes = []
    score = 0
    game_active = True

# Hlavní smyčka
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game_active:
                if event.key == pygame.K_SPACE:
                    bird_velocity = jump_strength  # skok
            else:
                if event.key == pygame.K_r:  # restart
                    reset_game()

    if game_active:
        # Pohyb ptáka
        bird_velocity += gravity
        bird_y += bird_velocity

        # Přidávání trubek
        if len(pipes) == 0 or pipes[-1][0] < WIDTH - 270:
            pipe_height = random.randint(100, HEIGHT - pipe_gap - 100)
            pipes.append([WIDTH, pipe_height, False])  # False = ještě nepočítané skóre

        # Pohyb trubek a kreslení
        screen.fill(BLUE)
        pygame.draw.circle(screen, YELLOW, (bird_x, int(bird_y)), bird_radius)

        for pipe in pipes:
            pipe[0] -= pipe_velocity
            pygame.draw.rect(screen, GREEN, (pipe[0], 0, pipe_width, pipe[1]))  # horní
            pygame.draw.rect(screen, GREEN, (pipe[0], pipe[1] + pipe_gap, pipe_width, HEIGHT - pipe[1] - pipe_gap))  # dolní

            # Kontrola kolize
            if (bird_x + bird_radius > pipe[0] and bird_x - bird_radius < pipe[0] + pipe_width):
                if bird_y - bird_radius < pipe[1] or bird_y + bird_radius > pipe[1] + pipe_gap:
                    game_active = False

            # Přičtení skóre, když pták projde trubkou
            if not pipe[2] and pipe[0] + pipe_width < bird_x:
                score += 1
                pipe[2] = True

        # Odstranění starých trubek
        pipes = [pipe for pipe in pipes if pipe[0] + pipe_width > 0]

        # Kolize se zemí nebo stropem
        if bird_y + bird_radius > HEIGHT or bird_y - bird_radius < 0:
            game_active = False

        # Skóre na obrazovce
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))

    else:
        # Game Over obrazovka
        screen.fill(BLUE)
        game_over_text = font.render("GAME OVER", True, RED)
        score_text = font.render("Score: " + str(score), True, WHITE)
        restart_text = font.render("Press R to restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 60))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 40))

    pygame.display.update()
    clock.tick(60)