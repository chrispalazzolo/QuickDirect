import pygame
import sys
from game_enums import GameStates, Directions
from game_globals import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, TILE_STEP, NUM_TILES_XY, DISPLAY_LINE, DISPLAY_HEIGHT_TOTAL, TILE_GAP_SIZE, BLACK, RED, REDHOVER, GREEN, GREENHOVER, GRAY, CHARCOAL, CELTICBLUE
from game_objects import GameBoard, Runner, Stopwatch, Counter, DirectionTarget, EndGameDisplay
from game_ui import Button
from game_fonts import TITLE_FONT, DISPLAY_FONT, BUTTON_FONT

from cProfile import Profile
from pstats import SortKey, Stats

def get_pos(tile):
    x = (tile[0] * TILE_STEP) + TILE_GAP_SIZE
    y = (tile[1] * TILE_STEP) + (DISPLAY_HEIGHT_TOTAL + TILE_GAP_SIZE)

    return x, y

def main():
    game_state = GameStates.INITIAL

    pygame.init()
    pygame.key.set_repeat(0)

    # Set up display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Quick Direct!')
    end_game_display = EndGameDisplay((SCREEN_WIDTH//2 , DISPLAY_HEIGHT_TOTAL))

    # Initialize game components
    stopwatch = Stopwatch((15, 10))
    counter = Counter((SCREEN_WIDTH - 100, 10))
    game_board = GameBoard(0, DISPLAY_HEIGHT_TOTAL, NUM_TILES_XY, CHARCOAL, TILE_SIZE, TILE_GAP_SIZE, GRAY)
    runner = Runner((TILE_GAP_SIZE, DISPLAY_HEIGHT_TOTAL + TILE_GAP_SIZE), (TILE_SIZE, TILE_SIZE), CELTICBLUE)
    target = DirectionTarget()
    
    # Control buttons
    start_button = Button(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 100, 40, "Start", GREEN, GREENHOVER)
    replay_button = Button(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 100, 40, "Play Again", RED, REDHOVER)
    
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
                    target.update((0, 0), (2, NUM_TILES_XY))
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
                        if direction_pressed == target.direction and runner.col_row == target.col_row:
                            if direction_pressed is Directions.UP:
                                col_row = 0
                                minmax = (0, target.col_row[1] - 1)
                            elif direction_pressed is Directions.DOWN:
                                col_row = 0
                                minmax = (target.col_row[1] + 1, NUM_TILES_XY - 1)
                            elif direction_pressed is Directions.LEFT:
                                col_row = 1
                                minmax = (0, target.col_row[0] - 1)
                            else: # Right
                                col_row = 1
                                minmax = (target.col_row[0] - 1, NUM_TILES_XY - 1)

                            target.update((col_row, target.col_row[col_row]), minmax)
                            runner.change_direction(direction_pressed)
                            counter.up()
                        else:
                            game_state = GameStates.ENDED
                            stopwatch.stop()

                            if direction_pressed != target.direction:
                                end_game_display.add("Wrong Direction!")
                            else:
                                end_game_display.add("Missed Direction!")

                            end_game_display.add("Direction Changes: " + str(counter.count))
                            end_game_display.add("Running Time: " + stopwatch.current_time)

                if event.type == pygame.KEYUP:
                    key_is_pressed = False
                    direction_pressed = Directions.NONE
            # If a game has been played and is now over, check to see if play again button has been clicked.
            elif game_state == GameStates.ENDED:
                if replay_button.is_clicked(event):
                    # Reset game components and change the state to PLAYING
                    key_is_pressed = False
                    game_state = GameStates.PLAYING
                    runner.reset()
                    target.reset()
                    target.update((0, 0), (2, NUM_TILES_XY))
                    stopwatch.reset()
                    counter.reset()
                    stopwatch.start()
                    end_game_display.reset()

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
                stopwatch.stop()
                end_game_display.add("Out of Bounds!")
                continue

            # Draw
            pygame.draw.line(screen, GRAY, (0, 50), (SCREEN_WIDTH, 50), DISPLAY_LINE)
            stopwatch.draw(screen)
            counter.draw(screen)
            game_board.draw(screen)
            target.draw(screen)
            runner.draw(screen)

        elif game_state == GameStates.ENDED:
            end_game_display.draw(screen)
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
