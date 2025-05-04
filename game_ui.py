import pygame
from game_settings import BLACK
from game_fonts import BUTTON_FONT

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.text_surf = BUTTON_FONT.render(text, True, BLACK)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        
    def draw(self, surface):
        # Check if mouse is hovering over button
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.current_color = self.hover_color
        else:
            self.current_color = self.color
            
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=8)  # Border
        surface.blit(self.text_surf, self.text_rect)
        
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
