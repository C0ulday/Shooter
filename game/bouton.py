import pygame

class Bouton:
    def __init__(self, x, y, text, font, font_size, color):
        self.x = x
        self.y = y
        self.text_str = text
        self.font = pygame.font.Font(font, font_size)
        self.color = color
        self.text_surface = self.font.render(self.text_str, True, color)
        self.text_rect = self.text_surface.get_rect(center=(self.x, self.y))
        
    def update(self, screen,position, color_pressed, color_not_pressed):
        self.changecolor(position, color_pressed, color_not_pressed)
        screen.blit(self.text_surface, self.text_rect)
        
        
    def boutonHover(self, position):
        # On vérifie si le clic se trouve dans le rectangle du texte
        if self.text_rect.collidepoint(position):
            return True
        return False
    
    def changecolor(self, position, color_pressed, color_not_pressed):
        if self.boutonHover(position):
            self.text_surface = self.font.render(self.text_str, True, color_pressed)
        else:
            self.text_surface = self.font.render(self.text_str, True, color_not_pressed)
