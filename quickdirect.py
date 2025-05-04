import pygame
import sys
import random
from enum import Enum
from game_settings import WIDTH, HEIGHT, TILE_SIZE, GAP_SIZE, BLACK, WHITE, RED, REDHOVER, GREEN, GREENHOVER, BLUE, GRAY, CHARCOAL, CELTICBLUE
from game_objects import Runner, Stopwatch, Counter
from game_ui import Button
from game_fonts import TITLE_FONT, DISPLAY_FONT, BUTTON_FONT

def draw_runner(surface, top_offset):
    rows = (HEIGHT - top_offset)//TILE_SIZE
    cols = WIDTH//TILE_SIZE
    gap = GAP_SIZE

    rand_row = random.randint(0, rows)
    rand_col = random.randint(0, cols)

    x_pos = rand_col * TILE_SIZE
    if rand_col > 0:
        x_pos += rand_col * GAP_SIZE

    y_pos = (rand_row * TILE_SIZE) + top_offset
    if rand_row > 0:
        y_pos += rand_col * GAP_SIZE

    # Temp Remove the following
    x_pos = 0
    y_pos = 0 + top_offset

    rect = pygame.Rect(x_pos, y_pos, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(surface, CELTICBLUE, rect)

def draw_board(surface, top_offset):
    tile_size = TILE_SIZE
    rows = (HEIGHT - top_offset)//tile_size
    cols = WIDTH//tile_size
    gap = GAP_SIZE

    for y in range(rows):
        y_pos = (y * tile_size) + top_offset
        if y > 0:
            y_pos += y * gap
        
        for x in range(cols):
            x_pos = x * tile_size
            if x > 0:
                x_pos += x * gap
            
            rect = pygame.Rect(x_pos, y_pos, tile_size, tile_size)
            pygame.draw.rect(surface, CHARCOAL, rect)

def main():
    class GameStates(Enum):
        INITIAL = 1
        PLAYING = 2
        ENDED = 3
    
    game_state = GameStates.INITIAL

    pygame.init()

    # Set up display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Quick Direct!')

    stopwatch = Stopwatch(15, 10)
    counter = Counter(WIDTH - 100, 10)
    runner = Runner(0, 0 + 50, TILE_SIZE, TILE_SIZE, CELTICBLUE)
    # Control buttons
    start_button = Button(WIDTH//2, HEIGHT//2, 100, 40, "Start", GREEN, GREENHOVER)
    replay_button = Button(WIDTH//2, HEIGHT//2, 100, 40, "Play Aagin", RED, REDHOVER)
    
    # Game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_state == GameStates.INITIAL:
                if start_button.is_clicked(event):
                    game_state = GameStates.PLAYING
                    stopwatch.start()
            
        if game_state == GameStates.INITIAL:
            # Update

            # Draw
            start_button.draw(screen)
        elif game_state == GameStates.PLAYING:
            # Update
            stopwatch.update()
            runner.update()

            # Draw
            screen.fill(BLACK)
            pygame.draw.line(screen, GRAY, (0, 50), (WIDTH, 50), 2)
            stopwatch.draw(screen)
            counter.draw(screen)
            top_offset = 53
            draw_board(screen,top_offset)
            #draw_runner(screen, top_offset)
            runner.draw(screen)
        
        # Update display
        pygame.display.flip()
        
        # Cap at 60 fps
        clock.tick(60)
    
    # Quit pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
