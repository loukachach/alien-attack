import pygame
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = (0, 255, 0)
BUTTON_HOVER_COLOR = (0, 200, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)
FPS = 60

# Game Constants
BLOCK_WIDTH = 20
BLOCK_HEIGHT = 20
PLAYER_COLOR = (0, 0, 255)  # Blue
ENEMY_COLOR = (0, 255, 0)  # Green
MOVE_VELOCITY = 10
PROJECTILE_VELOCITY = 15
PROJECTILE_WIDTH = 10
PROJECTILE_HEIGHT = 5
ENEMY_HEALTH = 3
ENEMY_SPAWN_INTERVAL = 5000  # in milliseconds
POINTS_PER_KILL = 10
COINS_PER_GAME = 100
COINS_UNLOCK_NEW_PLANE = 500
UNLOCKED_PLANES = 0

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Alien Attack")

# Fonts
font = pygame.font.Font(None, 30)
title_font = pygame.font.Font(None, 80)

# Coins
coins = 0

# Player
player = {
    "x": SCREEN_WIDTH // 2 - BLOCK_WIDTH // 2,
    "y": SCREEN_HEIGHT - BLOCK_HEIGHT - 10
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

# Game loop
running = True
while running:
    screen.fill(BACKGROUND_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                projectiles.append({
                    "x": player["x"] + BLOCK_WIDTH // 2,
                    "y": player["y"] - PROJECTILE_HEIGHT,
                    "vel": -PROJECTILE_VELOCITY
                })

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player["x"] > 0:
            player["x"] -= MOVE_VELOCITY
        if keys[pygame.K_RIGHT] and player["x"] < SCREEN_WIDTH - BLOCK_WIDTH:
            player["x"] += MOVE_VELOCITY

        # Update projectiles
        for projectile in projectiles:
            projectile["y"] += projectile["vel"]
            for enemy in enemies:
                if (
                        projectile["x"] >= enemy["x"]
                        and projectile["x"] <= enemy["x"] + BLOCK_WIDTH
                        and projectile["y"] <= enemy["y"] + BLOCK_HEIGHT
                ):
                    enemy["health"] -= 1
                    if enemy["health"] == 0:
                        enemies.remove(enemy)
                        points += POINTS_PER_KILL
                        kills += 1
                    projectiles.remove(projectile)
                    break

        # Spawn enemies
        current_time = pygame.time.get_ticks()
        if current_time >= enemy_spawn_time:
            x = random.randint(0, SCREEN_WIDTH - BLOCK_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT // 2)
            enemies.append({"x": x, "y": y, "health": ENEMY_HEALTH})
            enemy_spawn_time = current_time + ENEMY_SPAWN_INTERVAL

        # Draw player
        pygame.draw.rect(screen, PLAYER_COLOR, (player["x"], player["y"], BLOCK_WIDTH, BLOCK_HEIGHT))
        pygame.draw.rect(screen, (0, 0, 0), (player["x"], player["y"], BLOCK_WIDTH, 5))

        # Draw projectiles
        for projectile in projectiles:
            pygame.draw.rect(screen, (255, 0, 0),
                             (projectile["x"], projectile["y"], PROJECTILE_WIDTH, PROJECTILE_HEIGHT))

        # Draw enemies
        for enemy in enemies:
            pygame.draw.rect(screen, ENEMY_COLOR, (enemy["x"], enemy["y"], BLOCK_WIDTH, BLOCK_HEIGHT))
            pygame.draw.rect(screen, (255, 0, 0), (enemy["x"], enemy["y"] - 5, BLOCK_WIDTH, 3))
            pygame.draw.rect(screen, (0, 255, 0),
                             (enemy["x"], enemy["y"] - 5, BLOCK_WIDTH * (enemy["health"] / ENEMY_HEALTH), 3))

        # Draw score
        score_text = font.render(f"Points: {points}  Kills: {kills}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Check game over condition
        if kills >= 30:
            coins += COINS_PER_GAME
            game_over = True

    # Draw game over screen
    if game_over:
        game_over_text = title_font.render("Game Over!", True, (255, 255, 255))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))

    # Draw coins
    coins_text = font.render(f"Coins: {coins}", True, (255, 255, 255))
    screen.blit(coins_text, (SCREEN_WIDTH - coins_text.get_width() - 10, 10))

    pygame.display.update()

# Quit the game
pygame.quit()
