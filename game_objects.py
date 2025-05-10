# Game objects
import pygame
import time
import random
from game_enums import Directions
from game_globals import DISPLAY_HEIGHT_TOTAL, TILE_GAP_SIZE, TILE_STEP, WHITE, RED
from game_fonts import DISPLAY_FONT, TITLE_FONT

class Runner:
    def __init__(self, pos, dia, color):
        self.dia = dia
        self.start_xy = pos
        self.col_row = [0, 0]
        self.rect = pygame.Rect(pos[0], pos[1], dia[0], dia[1])
        self.color = color
        self.direction = Directions.DOWN
        self.speed = 1
        self.speed_limit = .035
        self.last_time = time.time()
    
    def init(self):
        self.direction = Directions.DOWN
        self.speed = 1
        self.col_row = [0, 0]
        self.speed_limit = .035
        self.last_time = time.time()

    def reset(self):
        self.init()
        self.rect.x = self.start_xy[0]
        self.rect.y = self.start_xy[1]

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
                    self.rect.y += TILE_STEP
                    self.col_row[1] += 1
                case Directions.UP:
                    self.rect.y -= TILE_STEP
                    self.col_row[1] -= 1
                case Directions.LEFT:
                    self.rect.x -= TILE_STEP
                    self.col_row[0] -= 1
                case Directions.RIGHT:
                    self.rect.x += TILE_STEP
                    self.col_row[0] += 1

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class DirectionTarget:
    def __init__(self):
        self.img = pygame.image.load("arrow.png")
        self.pos = [TILE_GAP_SIZE, DISPLAY_HEIGHT_TOTAL + TILE_GAP_SIZE]
        self.direction = Directions.DOWN
        self.angle = 0
        self.col_row = [0, 0]

    def rotate_arrow(self):
        self.img = pygame.transform.rotate(self.img, -self.angle)
        if self.direction != Directions.UP:
            self.img = pygame.transform.rotate(self.img, self.direction.value)
        self.angle = self.direction.value

    def get_next_direction(self, traveling, minmax):
        if traveling[0] == 0: # col, can be left or right
            if traveling[1] == 0:
                return Directions.RIGHT
            if traveling[1] == minmax[1]:
                return Directions.LEFT

            valid_directions = [Directions.LEFT, Directions.RIGHT]

        else: # row, can be Up or Down
            if traveling[1] == 0:
                return Directions.DOWN
            if traveling[1] == minmax[1]:
                return Directions.UP

            valid_directions = [Directions.DOWN, Directions.UP]

        return random.choice(valid_directions)

    def update_pos(self):
        self.pos[0] = (self.col_row[0] * TILE_STEP) + TILE_GAP_SIZE
        self.pos[1] = (self.col_row[1] * TILE_STEP) + (DISPLAY_HEIGHT_TOTAL + TILE_GAP_SIZE)

    def update(self, traveling, minmax):
        new_col_row = random.randint(minmax[0], minmax[1])
        self.col_row[0 if traveling[0] == 1 else 1] = new_col_row  # traveling[0], value: 0 = col, 1 = row
        self.direction = self.get_next_direction(traveling, minmax)
        self.rotate_arrow()
        self.update_pos()

    def reset(self):

        self.col_row = [0, 0]

    def draw(self, surface):
        surface.blit(self.img, self.pos)

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
    def __init__(self, pos):
        self.pos = pos
        self.elapsed_time = 0
        self.start_time = 0
        self.current_time = "00:00:00"
        self.running = False
        
    def update(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            minutes = int(self.elapsed_time // 60)
            seconds = int(self.elapsed_time % 60)
            centiseconds = int((self.elapsed_time % 1) * 100)
            self.current_time = f"{minutes:02d}:{seconds:02d}.{centiseconds:02d}"
                
    def draw(self, surface):
        # Draw timer display
        timer_surf = DISPLAY_FONT.render(self.current_time, True, WHITE)
        timer_rect = timer_surf.get_rect(topleft=(self.pos[0], self.pos[1]))
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
        self.current_time = "00:00:00"

class Counter:
    def __init__(self, pos):
        self.pos = pos
        self.count = 0
    
    def up(self):
        self.count += 1

    def down(self):
        self.count -= 1
    
    def reset(self):
        self.count = 0

    def draw(self, surface):
        surf = DISPLAY_FONT.render("Count: " + str(self.count), True, WHITE)
        rect = surf.get_rect(topleft=(self.pos[0] - 80, self.pos[1]))
        surface.blit(surf, rect)

class EndGameDisplay:
    def __init__(self, pos):
        self.game_over_str = "Game Over"
        self.captions = []
        self.pos = pos

    def reset(self):
        self.captions = []

    def add(self, txt):
        self.captions.append(txt)

    def draw(self, surface):
        x = self.pos[0]
        y = self.pos[1]
        line_height = 30

        surf = TITLE_FONT.render(self.game_over_str, True, RED)
        rect = surf.get_rect(center=(x, y))
        surface.blit(surf, rect)
        y += line_height * 2

        for txt in self.captions:
            surf = DISPLAY_FONT.render(txt, True, WHITE)
            rect = surf.get_rect(center= (x, y))
            surface.blit(surf, rect)
            y += line_height
