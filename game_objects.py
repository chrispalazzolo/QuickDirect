# Game objects
import pygame
import time
import random
from game_enums import Directions
from game_settings import SCREEN_WIDTH, SCREEN_HEIGHT, DISPLAY_HEIGHT, TILE_SIZE, TILE_GAP_SIZE, WHITE
from game_fonts import DISPLAY_FONT, TITLE_FONT

class Runner:
    def __init__(self, x, y, width, height, color):
        self.width = width
        self.height = height
        self.start_x = x
        self.start_y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.init()
    
    def init(self):
        self.direction = Directions.DOWN
        self.speed = 1
        self.speed_limit = .035
        self.last_time = time.time()

    def reset(self):
        self.init()
        self.rect.x = self.start_x
        self.rect.y = self.start_y

    def inc_speed(self):
        inc_by = .2
        if self.speed > self.speed_limit:
            if self.speed > .7:
                inc_by = .2
            elif self.speed > .4:
                inc_by = .1
            else:
                inc_by = .01
            
            self.speed -= inc_by
        else:
            self.speed = self.speed_limit
        
        #print("Speed:", self.speed)

    def change_direction(self, direction):
        self.direction = direction
        self.inc_speed()

    def update(self):
        current_time = time.time()
        if current_time - self.last_time >= self.speed:
            self.last_time = current_time

            match self.direction:
                case Directions.DOWN:
                    self.rect.y += self.height + TILE_GAP_SIZE
                case Directions.UP:
                    self.rect.y -= self.height + TILE_GAP_SIZE
                case Directions.LEFT:
                    self.rect.x -= self.width + TILE_GAP_SIZE
                case Directions.RIGHT:
                    self.rect.x += self.width + TILE_GAP_SIZE

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class DirectionTile:
    def __init__(self, position, constraints, direction):
        self.x = position[0]
        self.y = position[1]
        self.row_first = constraints[0]
        self.row_last = constraints[1]
        self.col_first = constraints[2]
        self.col_last = constraints[3]
        self.direction = direction
        self.rect = pygame.Rect(position[0], position[1], TILE_SIZE, TILE_SIZE)
    
    def place(self, row, col, constraint):
        rand_num = random.randint(constraint[0], constraint[1])

        if row > -1:
            new_row = row
            new_col = rand_num
        elif col > -1:
            new_col = col
            new_row = rand_num
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class GameBoard:
    def __init__(self, x, y, num_tiles_xy, color, tile_size, tile_gap_size, tile_gap_color):
        self.x = x
        self.y = y
        self.num_tiles_xy = num_tiles_xy
        self.width = (num_tiles_xy * (tile_size + tile_gap_size)) + (tile_gap_size * 2)
        self.height = self.width
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = color
        self.tile_size = tile_size
        self.tile_gap_size = tile_gap_size
        self.tile_gap_color = tile_gap_color
        self.x_lines = [] # Holds the coords and size of line
        self.y_lines = []
        self.calculate_board_lines()

    def calculate_board_lines(self):
        tile_and_gap_size = self.tile_size + self.tile_gap_size
        start_y = self.y
        end_y = self.y + self.height
        start_x = self.x
        end_x = self.x + self.width
        next_pos = 0

        self.x_lines.append(((next_pos, start_y), (next_pos, end_y)))
        for x in range(self.num_tiles_xy):
            next_pos += tile_and_gap_size
            self.x_lines.append(((next_pos, start_y), (next_pos, end_y)))
        
        next_pos = start_y 

        self.y_lines.append(((start_x, next_pos), (end_x, next_pos)))
        for y in range(self.num_tiles_xy):
            next_pos += tile_and_gap_size
            self.y_lines.append(((start_x, next_pos), (end_x, next_pos)))

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

        for line_data in self.x_lines:
            pygame.draw.line(surface, self.tile_gap_color, line_data[0], line_data[1], self.tile_gap_size)
        
        for line_data in self.y_lines:
            pygame.draw.line(surface, self.tile_gap_color, line_data[0], line_data[1], self.tile_gap_size)

class Stopwatch:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.elapsed_time = 0
        self.start_time = 0
        self.running = False
        #self.title_surf = TITLE_FONT.render("Stopwatch", True, WHITE)
        #self.title_rect = self.title_surf.get_rect(center=(x, y - 80))
        
    def update(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
                
    def draw(self, surface):
        # Draw title
        #surface.blit(self.title_surf, self.title_rect)
        
        # Draw timer display
        minutes = int(self.elapsed_time // 60)
        seconds = int(self.elapsed_time % 60)
        centiseconds = int((self.elapsed_time % 1) * 100)
        time_str = f"{minutes:02d}:{seconds:02d}.{centiseconds:02d}"
            
        timer_surf = DISPLAY_FONT.render(time_str, True, WHITE)
        timer_rect = timer_surf.get_rect(topleft=(self.x, self.y))
        surface.blit(timer_surf, timer_rect)

    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True

    def stop(self):
        if self.running:
            self.running = False
    
    def reset(self):
        self.running = False
        self.elapsed_time = 0

class Counter:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.count = 0
        self.title_surf = DISPLAY_FONT.render("Count:", True, WHITE)
        self.title_rect = self.title_surf.get_rect(topleft=(x - 80, y))
    
    def up(self):
        self.count += 1

    def down(self):
        self.count -= 1
    
    def reset(self):
        self.count = 0

    def draw(self, surface):
        surface.blit(self.title_surf, self.title_rect)
        counter_surf = DISPLAY_FONT.render(str(self.count), True, WHITE)
        counter_rect = counter_surf.get_rect(topleft=(self.x, self.y))
        surface.blit(counter_surf, counter_rect)