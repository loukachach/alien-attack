import pygame

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Alien Killer")
    clock = pygame.time.Clock()

    title_font = pygame.font.Font(None, 64)
    title_text = title_font.render("Alien Killer", True, TITLE_COLOR)
    title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))

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

        # Draw the title
        screen.blit(title_text, title_text_rect)

        mouse_pos = pygame.mouse.get_pos()
        draw_button(screen, play_button_rect, "Play", play_button_rect.collidepoint(mouse_pos))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
