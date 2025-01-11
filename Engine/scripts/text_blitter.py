from pygame.font import Font

class TextBlitter:
    def __init__(self, font=None, size=25):
        self.reset()
        self.font = Font(font, size)
        
        self.x = ...
        self.y = ...
        self.line_height = ...
    
    def tprint(self, screen, text, antialias, color='black'):
        text_bitmap = self.font.render(text, antialias, color)
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height
    
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
    
    def indent(self):
        self.x += 10
    
    def unindent(self):
        self.x -= 10
