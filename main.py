#!/usr/bin/python


import pygame
import random

# Constants
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = (0, 255, 0)
BUTTON_HOVER_COLOR = (0, 200, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)
FPS = 60

# Game Constants
BLOCK_SIZE = 40
PLAYER_COLOR = (128, 128, 128)  # Gray
ENEMY_COLOR = (0, 255, 0)  # Green
MOVE_VELOCITY = 2  # Adjusted for slower motion
PROJECTILE_VELOCITY = 7  # Adjusted for slower projectile speed
PROJECTILE_WIDTH = 10
PROJECTILE_HEIGHT = 5
ENEMY_HEALTH = 1
ENEMY_SPAWN_INTERVAL = 2000  # in milliseconds
POINTS_PER_KILL = 10
PLAYER_LIFE_POINTS = 3


# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Alien Attack")

# Fonts
font = pygame.font.Font(None, 30)
title_font = pygame.font.Font(None, 80)

# Player
player = {
    "x": SCREEN_WIDTH // 2,
    "y": SCREEN_HEIGHT - BLOCK_SIZE - 10,
    "life_points": PLAYER_LIFE_POINTS
}

# Projectiles
projectiles = []

# Enemies
enemies = []
enemy_spawn_time = pygame.time.get_ticks() + ENEMY_SPAWN_INTERVAL

# Game variables
points = 0
kills = 0
game_over = False

# Life Bar
LIFE_BAR_WIDTH = 100
LIFE_BAR_HEIGHT = 10

# Main menu
def main_menu():
    global points, kills, game_over, player, projectiles, enemies, enemy_spawn_time
    while True:
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(mouse_pos):
                    points = 0
                    kills = 0
                    game_over = False
                    player = {
                        "x": SCREEN_WIDTH // 2,
                        "y": SCREEN_HEIGHT - BLOCK_SIZE - 10,
                        "life_points": PLAYER_LIFE_POINTS
                    }
                    projectiles = []
                    enemies = []
                    enemy_spawn_time = pygame.time.get_ticks() + ENEMY_SPAWN_INTERVAL
                    run_game()
        # Play button
        play_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT)
        draw_button(screen, play_button_rect, "Play", play_button_rect.collidepoint(pygame.mouse.get_pos()))

        pygame.display.update()



# Function to draw a button on the screen
def draw_button(screen, button_rect, button_text, is_hovered):
    button_color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, button_rect)
    font = pygame.font.Font(None, 32)
    text = font.render(button_text, True, BUTTON_TEXT_COLOR)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

# Game loop
def run_game():
    global points, kills, player, projectiles, enemies, enemy_spawn_time, game_over

    # Game loop
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    projectiles.append({
                        "x": player["x"],
                        "y": player["y"] - PROJECTILE_HEIGHT,
                        "vel": -PROJECTILE_VELOCITY
                    })
            elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
                mouse_pos = pygame.mouse.get_pos()
                if go_back_button_rect.collidepoint(mouse_pos):
                    return

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player["x"] > 0:
                player["x"] -= MOVE_VELOCITY
            if keys[pygame.K_RIGHT] and player["x"] < SCREEN_WIDTH - BLOCK_SIZE:
                player["x"] += MOVE_VELOCITY

            # Update projectiles
            for projectile in projectiles:
                projectile["y"] += projectile["vel"]
                for enemy in enemies:
                    if (
                            projectile["x"] >= enemy["x"]
                            and projectile["x"] <= enemy["x"] + BLOCK_SIZE
                            and projectile["y"] <= enemy["y"] + BLOCK_SIZE
                    ):
                        enemy["health"] -= 1
                        if enemy["health"] <= 0:
                            enemies.remove(enemy)
                            points += POINTS_PER_KILL
                            kills += 1
                            if kills % 10 == 0:
                                player["life_points"] += 1
                        projectiles.remove(projectile)
                        break

            # Move enemies down
            for enemy in enemies:
                enemy["y"] += MOVE_VELOCITY // 2

                if enemy["y"] >= SCREEN_HEIGHT:
                    player["life_points"] -= 1
                    enemies.remove(enemy)

            # Spawn enemies
            current_time = pygame.time.get_ticks()
            if current_time >= enemy_spawn_time:
                x = random.randint(0, SCREEN_WIDTH - BLOCK_SIZE)
                y = 0
                enemies.append({
                    "x": x,
                    "y": y,
                    "health": ENEMY_HEALTH
                })
                enemy_spawn_time = current_time + ENEMY_SPAWN_INTERVAL

            # Draw player
            pygame.draw.polygon(screen, PLAYER_COLOR, [
                (player["x"], player["y"]),
                (player["x"] + BLOCK_SIZE, player["y"]),
                (player["x"] + BLOCK_SIZE // 2, player["y"] - BLOCK_SIZE)
            ])

            # Draw projectiles
            for projectile in projectiles:
                pygame.draw.rect(screen, (255, 0, 0),
                                 (projectile["x"], projectile["y"], PROJECTILE_WIDTH, PROJECTILE_HEIGHT))

            # Draw enemies
            for enemy in enemies:
                pygame.draw.rect(screen, ENEMY_COLOR,
                                 (enemy["x"], enemy["y"], BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, (255, 0, 0),
                                 (enemy["x"], enemy["y"] - 5, BLOCK_SIZE, 3))
                pygame.draw.rect(screen, (0, 255, 0),
                                 (enemy["x"], enemy["y"] - 5, BLOCK_SIZE * (enemy["health"] / ENEMY_HEALTH), 3))

            # Draw score
            score_text = font.render(f"Score: {points}  Kills: {kills}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            # Draw life bar
            life_bar_x = SCREEN_WIDTH - LIFE_BAR_WIDTH - 10
            life_bar_y = 10
            life_bar_width = int(player["life_points"] / PLAYER_LIFE_POINTS * LIFE_BAR_WIDTH)
            pygame.draw.rect(screen, (255, 0, 0), (life_bar_x, life_bar_y, LIFE_BAR_WIDTH, LIFE_BAR_HEIGHT))
            pygame.draw.rect(screen, (0, 255, 0), (life_bar_x, life_bar_y, life_bar_width, LIFE_BAR_HEIGHT))

            # Check game over condition
            if player["life_points"] <= 0:
                game_over = True

        else:
            # Game over screen
            game_over_text = title_font.render("Game Over", True, (255, 0, 0))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))

            go_back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 300, BUTTON_WIDTH, BUTTON_HEIGHT)
            draw_button(screen, go_back_button_rect, "Go Back to Lobby",
                        go_back_button_rect.collidepoint(pygame.mouse.get_pos()))

        pygame.display.update()

# Run the main menu
main_menu()
