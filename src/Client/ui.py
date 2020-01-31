import pygame

pygame.font.init()

TOP_MARGIN = 10
RIGHT_MARGIN = 30
BUTTON_MARGIN_H = 20

class Button:
    def __init__(self, x,y,w,h, callback, color, text, size):
        self.x,self.y = x,y
        self.w,self.h = w,h
        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)
        self.callback = callback
        self.color = color

        self.text = Text(self.x + self.w / 2, self.y + self.h / 2, text, size, True)

    def draw(self,game):
        pygame.draw.rect(game.blitting_surface, self.color, (self.x,self.y,self.w,self.h))
        self.text.draw(game)

class Text:
    def __init__(self, x,y, text, size, center=False):
        self.x,self.y = x,y

        font = pygame.font.SysFont("Arial", size)
        self.surface = font.render(text, 1, (255,255,255))
        self.height = self.surface.get_height()

        if center:
            self.x -= self.surface.get_width() / 2
            self.y -= self.surface.get_height() / 2

    def draw(self, game):
        game.blitting_surface.blit(self.surface, (self.x, self.y))

class StrategyChooser:
    def __init__(self, x,y,w,h):
        self.x,self.y = x,y
        self.w,self.h = w,h
        self.total_height = 0
        self.tittle = self.add_text("Choose a strategy.", 52)
        self.buttons = []

        self.show = True

    def draw(self, game):
        if not self.show: return
        pygame.draw.rect(game.blitting_surface, (192,192,192), (self.x,self.y,self.w,self.h))
        [e.draw(game) for e in self.buttons + [self.tittle]]

    def add_text(self, text, size):
        text_obj = Text(
                    self.x + RIGHT_MARGIN, self.y + self.total_height + TOP_MARGIN,
                    text, size
                )
        self.total_height += (text_obj.height + BUTTON_MARGIN_H)
        return text_obj

    def add_button(self, callback, button_w, button_h, color, text, size):
        x = self.x + RIGHT_MARGIN
        y = self.y + self.total_height + TOP_MARGIN
        self.buttons.append(Button(x,y,button_w,button_h, callback, color, text, size))
        self.total_height += button_h + BUTTON_MARGIN_H

    def update(self, mouse_position):
        if not self.show: return
        for btn in self.buttons:
            if btn.rect.collidepoint(mouse_position):
                btn.callback()

    def toggle(self):
        self.show = not self.show
