# Game objects

import pygame
import time
from game_settings import WIDTH, HEIGHT, TILE_SIZE, GAP_SIZE, WHITE
from game_fonts import DISPLAY_FONT, TITLE_FONT

class Runner:
    def __init__(self, x, y, width, height, color):
        self.width = width
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.direction = 0
        self.speed = 1
        self.last_time = time.time()
    
    def inc_speed(self):
        self.speed -= .1

    def update(self):
        current_time = time.time()
        if current_time - self.last_time >= 1.0:
            self.last_time = current_time
            self.rect.y += self.width + GAP_SIZE

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

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