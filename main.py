import pygame
from game_state import GameState

pygame.init()

# Window setup
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 32)
font_level = pygame.font.SysFont(None, 28)

# Sounds
correct_sound = pygame.mixer.Sound("correct.wav")
wrong_sound = pygame.mixer.Sound("wrong.wav")

# Game state
game = GameState()
current_pos = list(game.start)
game.user_path.append(tuple(current_pos))
game_over = False
show_next_level = False
next_level_time = 0
solution_index = 0  # For animating the correct path on failure

def draw_maze():
    rows, cols = game.height, game.width
    cell_w = WINDOW_WIDTH // cols
    cell_h = WINDOW_HEIGHT // rows

    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(x * cell_w, y * cell_h, cell_w, cell_h)
            color = (255, 255, 255) if game.maze[y][x] == 0 else (0, 0, 0)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (50, 50, 50), rect, 1)  # Grid lines

    # Draw user path
    for y, x in game.user_path:
        pygame.draw.rect(screen, (0, 200, 255), (x * cell_w, y * cell_h, cell_w, cell_h))

    # Draw solution if game over
    if game_over:
        for i in range(min(solution_index, len(game.solution))):
            y, x = game.solution[i]
            pygame.draw.rect(screen, (255, 100, 100), (x * cell_w, y * cell_h, cell_w, cell_h))

    # Start and end
    sy, sx = game.start
    ey, ex = game.end
    pygame.draw.rect(screen, (0, 255, 0), (sx * cell_w, sy * cell_h, cell_w, cell_h))  # Start
    pygame.draw.rect(screen, (255, 100, 0), (ex * cell_w, ey * cell_h, cell_w, cell_h))  # End

    # Current position
    cy, cx = current_pos
    pygame.draw.rect(screen, (255, 255, 0), (cx * cell_w, cy * cell_h, cell_w, cell_h))

def draw_text_label(text, x, y, font, color):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def draw_popup(title, subtitle, title_color, subtitle_color):
    popup_width, popup_height = 400, 150
    popup_x = (WINDOW_WIDTH - popup_width) // 2
    popup_y = (WINDOW_HEIGHT - popup_height) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

    # Semi-transparent background
    s = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    s.fill((30, 30, 30, 200))  # RGBA
    screen.blit(s, (popup_x, popup_y))

    # Border
    pygame.draw.rect(screen, (200, 200, 200), popup_rect, 2, border_radius=10)

    # Title
    title_surface = font.render(title, True, title_color)
    title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, popup_y + 45))
    screen.blit(title_surface, title_rect)

    # Subtitle
    subtitle_surface = font_small.render(subtitle, True, subtitle_color)
    subtitle_rect = subtitle_surface.get_rect(center=(WINDOW_WIDTH // 2, popup_y + 100))
    screen.blit(subtitle_surface, subtitle_rect)

running = True
while running:
    screen.fill((0, 0, 0))
    draw_maze()
    draw_text_label(f"Level {game.level}", 10, 10, font_level, (255, 255, 255))

    if game_over:
        draw_popup("Game Over!", "Press R to Restart", (255, 80, 80), (220, 220, 220))
        if solution_index < len(game.solution):
            solution_index += 1

    elif show_next_level:
        draw_popup("Level Completed!", f"Next: Level {game.level + 1}", (80, 255, 80), (200, 200, 200))
        if pygame.time.get_ticks() - next_level_time > 2000:
            show_next_level = False
            game.next_level()
            current_pos = list(game.start)
            game.user_path = [tuple(current_pos)]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over and not show_next_level and event.type == pygame.KEYDOWN:
            y, x = current_pos
            ny, nx = y, x

            if event.key == pygame.K_UP:
                ny -= 1
            elif event.key == pygame.K_DOWN:
                ny += 1
            elif event.key == pygame.K_LEFT:
                nx -= 1
            elif event.key == pygame.K_RIGHT:
                nx += 1
            elif event.key == pygame.K_BACKSPACE:
                if len(game.user_path) > 1:
                    game.user_path.pop()
                    current_pos[0], current_pos[1] = game.user_path[-1]
                continue

            if 0 <= ny < game.height and 0 <= nx < game.width:
                if game.maze[ny][nx] == 0 and (ny, nx) not in game.user_path:
                    current_pos[0], current_pos[1] = ny, nx
                    game.user_path.append((ny, nx))

            if event.key == pygame.K_RETURN:
                if game.submit():
                    correct_sound.play()
                    show_next_level = True
                    next_level_time = pygame.time.get_ticks()
                else:
                    wrong_sound.play()
                    game_over = True
                    solution_index = 0

        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            game = GameState()
            current_pos = list(game.start)
            game.user_path = [tuple(current_pos)]
            game_over = False
            solution_index = 0

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
