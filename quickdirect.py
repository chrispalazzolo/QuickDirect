import pygame
import sys
import random
from game_enums import GameStates, Directions
from game_settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, NUM_TILES_XY, DISPLAY_HEIGHT, DISPLAY_LINE, DISPLAY_HEIGHT_TOTAL, TILE_GAP_SIZE, BLACK, WHITE, RED, REDHOVER, GREEN, GREENHOVER, BLUE, GRAY, CHARCOAL, CELTICBLUE
from game_objects import GameBoard, Runner, Stopwatch, Counter, DirectionTarget
from game_ui import Button
from game_fonts import TITLE_FONT, DISPLAY_FONT, BUTTON_FONT

from cProfile import Profile
from pstats import SortKey, Stats

def check_move_request(input_dir, runner_pos, target_pos, target_dir):
     return input_dir == target_dir and runner_pos == target_pos

def main():
    game_state = GameStates.INITIAL

    pygame.init()
    pygame.key.set_repeat(0)

    # Set up display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Quick Direct!')

    # Initialize game components
    stopwatch = Stopwatch(15, 10)
    counter = Counter(SCREEN_WIDTH - 100, 10)
    game_board = GameBoard(0, DISPLAY_HEIGHT_TOTAL, NUM_TILES_XY, CHARCOAL, TILE_SIZE, TILE_GAP_SIZE, GRAY)
    runner = Runner(TILE_GAP_SIZE, DISPLAY_HEIGHT_TOTAL + TILE_GAP_SIZE, TILE_SIZE, TILE_SIZE, CELTICBLUE)
    target = DirectionTarget((TILE_GAP_SIZE, DISPLAY_HEIGHT_TOTAL + TILE_GAP_SIZE), NUM_TILES_XY)
    
    # Control buttons
    start_button = Button(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 100, 40, "Start", GREEN, GREENHOVER)
    replay_button = Button(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 100, 40, "Play Aagin", RED, REDHOVER)
    
    # Game loop
    clock = pygame.time.Clock()
    running = True
    key_is_pressed = False # To stop key press repeating if key is held down
    direction_pressed = Directions.NONE

    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # When game first loads, check if the start button has been clicked.
            if game_state == GameStates.INITIAL:
                if start_button.is_clicked(event):
                    game_state = GameStates.PLAYING
                    stopwatch.start()
            # While a game is currently in play, check if any directional keys have been pressed.
            elif game_state == GameStates.PLAYING:
                if event.type == pygame.KEYDOWN and not key_is_pressed:
                    key_is_pressed = True
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_UP] or keys[pygame.K_w]:
                        direction_pressed = Directions.UP
                    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                        direction_pressed = Directions.DOWN
                    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                        direction_pressed = Directions.LEFT
                    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                        direction_pressed = Directions.RIGHT

                    if direction_pressed is not Directions.NONE:
                        if check_move_request():
                            target.update()
                            runner.change_direction(direction_pressed)
                            counter.up()
                        else:
                            game_state = GameStates.ENDED

                if event.type == pygame.KEYUP:
                    key_is_pressed = False
                    direction_pressed = Directions.NONE
            # If a game has been played and is now over, check to see if play again button has been clicked.
            elif game_state == GameStates.ENDED:
                if replay_button.is_clicked(event):
                    # Reset game components and change the state to PLAYING
                    game_state = GameStates.PLAYING
                    runner.reset()
                    stopwatch.reset()
                    counter.reset()
                    stopwatch.start()

        screen.fill(BLACK)

        if game_state == GameStates.INITIAL:
            # Update

            # Draw
            start_button.draw(screen)
        elif game_state == GameStates.PLAYING:
            # Update
            stopwatch.update()
            runner.update()
            
            if (runner.rect.x < 0 or runner.rect.x >= SCREEN_WIDTH) or (runner.rect.y < DISPLAY_HEIGHT_TOTAL or runner.rect.y >= SCREEN_HEIGHT):
                game_state = GameStates.ENDED
                continue
            
            # Draw
            pygame.draw.line(screen, GRAY, (0, 50), (SCREEN_WIDTH, 50), DISPLAY_LINE)
            stopwatch.draw(screen)
            counter.draw(screen)
            game_board.draw(screen)
            target.draw(screen)
            runner.draw(screen)

        elif game_state == GameStates.ENDED:
            replay_button.draw(screen)

        # Update display
        pygame.display.flip()
        
        # Cap at 60 fps
        clock.tick(60)
    
    # Quit pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
