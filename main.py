import pygame

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = (0, 255, 0)
BUTTON_HOVER_COLOR = (0, 200, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)
TITLE_COLOR = (255, 255, 255)
FPS = 60



def draw_button(screen, button_rect, button_text, is_hovered):
    button_color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, button_rect)
    font = pygame.font.Font(None, 32)
    text = font.render(button_text, True, BUTTON_TEXT_COLOR)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)


def play_game():
    print("Starting the game...")
    import pygame
    import random

    # Constants
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 500
    BLOCK_WIDTH = 20
    BLOCK_HEIGHT = 20
    PLAYER_COLOR = (128, 128, 128)  # Gray
    ENEMY_COLOR = (0, 0, 255)  # Blue
    BACKGROUND_COLOR = (0, 0, 0)
    MOVE_VELOCITY = 10
    PROJECTILE_VELOCITY = 15
    PROJECTILE_WIDTH = 10
    PROJECTILE_HEIGHT = 5
    PROJECTILE_COLOR = (255, 0, 0)
    ENEMY_HEALTH = 3
    ENEMY_SPAWN_INTERVAL = 5000  # in milliseconds
    POINTS_PER_KILL = 10

    class Enemy:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.health = ENEMY_HEALTH

        def hit(self):
            self.health -= 1
            if self.health == 0:
                return True
            return False

    def handle_events(player, projectiles):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    projectiles.append({
                        "x": player["x"] + BLOCK_WIDTH // 2,
                        "y": player["y"] - PROJECTILE_HEIGHT,
                        "vel": -PROJECTILE_VELOCITY
                    })
        return True

    def update_projectiles(projectiles, enemies, points, kills):
        for projectile in projectiles:
            projectile["y"] += projectile["vel"]
            for enemy in enemies:
                if (
                        projectile["x"] >= enemy.x
                        and projectile["x"] <= enemy.x + BLOCK_WIDTH
                        and projectile["y"] <= enemy.y + BLOCK_HEIGHT
                ):
                    if enemy.hit():
                        enemies.remove(enemy)
                        points += POINTS_PER_KILL
                        kills += 1
                    projectiles.remove(projectile)
                    break
        # Remove projectiles that have gone off-screen
        projectiles[:] = [p for p in projectiles if p["y"] > 0]
        return points, kills

    def draw_player(screen, player):
        pygame.draw.polygon(screen, PLAYER_COLOR, [
            (player["x"] + BLOCK_WIDTH // 2, player["y"]),
            (player["x"], player["y"] + BLOCK_HEIGHT),
            (player["x"] + BLOCK_WIDTH, player["y"] + BLOCK_HEIGHT)
        ])
        pygame.draw.rect(screen, (0, 0, 0), (player["x"], player["y"], BLOCK_WIDTH, 5))

    def draw_projectiles(screen, projectiles):
        for projectile in projectiles:
            pygame.draw.rect(screen, PROJECTILE_COLOR,
                             (projectile["x"], projectile["y"], PROJECTILE_WIDTH, PROJECTILE_HEIGHT))

    def draw_enemies(screen, enemies):
        for enemy in enemies:
            pygame.draw.rect(screen, ENEMY_COLOR, (enemy.x, enemy.y, BLOCK_WIDTH, BLOCK_HEIGHT))
            pygame.draw.rect(screen, (255, 0, 0), (enemy.x, enemy.y - 5, BLOCK_WIDTH, 3))
            pygame.draw.rect(screen, (0, 255, 0),
                             (enemy.x, enemy.y - 5, BLOCK_WIDTH * (enemy.health / ENEMY_HEALTH), 3))

    def spawn_enemy(enemies):
        x = random.randint(0, SCREEN_WIDTH - BLOCK_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT // 2)
        enemies.append(Enemy(x, y))

    def draw_score(screen, points, kills):
        font = pygame.font.Font(None, 30)
        text = font.render(f"Points: {points}  Kills: {kills}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

    def run_game():
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Moving and Shooting Block")
        player = {
            "x": SCREEN_WIDTH // 2 - BLOCK_WIDTH // 2,
            "y": SCREEN_HEIGHT - BLOCK_HEIGHT - 10
        }
        projectiles = []
        enemies = []
        enemy_spawn_time = pygame.time.get_ticks() + ENEMY_SPAWN_INTERVAL
        points = 0
        kills = 0
        run = True
        while run:
            pygame.time.delay(10)
            run = handle_events(player, projectiles)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player["x"] > 0:
                player["x"] -= MOVE_VELOCITY
            if keys[pygame.K_RIGHT] and player["x"] < SCREEN_WIDTH - BLOCK_WIDTH:
                player["x"] += MOVE_VELOCITY
            points, kills = update_projectiles(projectiles, enemies, points, kills)
            screen.fill(BACKGROUND_COLOR)
            draw_player(screen, player)
            draw_projectiles(screen, projectiles)
            draw_enemies(screen, enemies)
            draw_score(screen, points, kills)
            pygame.display.update()

            # Check if it's time to spawn a new enemy
            current_time = pygame.time.get_ticks()
            if current_time >= enemy_spawn_time:
                spawn_enemy(enemies)
                enemy_spawn_time = current_time + ENEMY_SPAWN_INTERVAL

        pygame.quit()

    if __name__ == "__main__":
        run_game()


def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("alien attack")
    clock = pygame.time.Clock()

    play_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT)
    scores_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 275, BUTTON_WIDTH, BUTTON_HEIGHT)
    credits_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 350, BUTTON_WIDTH, BUTTON_HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(mouse_pos):
                    play_game()
                elif scores_button_rect.collidepoint(mouse_pos):
                    print("Scores button clicked!")
                elif credits_button_rect.collidepoint(mouse_pos):
                    print("Credits button clicked!")

        screen.fill(BACKGROUND_COLOR)
        mouse_pos = pygame.mouse.get_pos()
        draw_button(screen, play_button_rect, "Play", play_button_rect.collidepoint(mouse_pos))


        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main_menu()
