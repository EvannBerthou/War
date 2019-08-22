import pygame

pygame.font.init()

TOP_MARGIN = 5
RIGHT_MARGIN = 15
BUTTON_MARGIN_H = 10

class Button:
    def __init__(self, x,y,w,h, callback, color, text, size):
        self.x,self.y = x,y
        self.w,self.h = w,h
        self.callback = callback
        self.color = color

        self.text = Text(self.x + self.w / 2, self.y + self.h / 2, text, size, True)

    def draw(self,game):
        pygame.draw.rect(game.win, self.color, (self.x,self.y,self.w,self.h))
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
        game.win.blit(self.surface, (self.x, self.y))

class StrategyChooser:
    def __init__(self, x,y,w,h):
        self.x,self.y = x,y
        self.w,self.h = w,h
        self.elements = []
        self.total_height = 0

        self.add_text("Choose a strategy.", 28)

    def draw(self, game):
        pygame.draw.rect(game.win, (192,192,192), (self.x,self.y,self.w,self.h))
        [e.draw(game) for e in self.elements]

    def add_text(self, text, size):
        text_obj = Text(
                    self.x + RIGHT_MARGIN, self.y + self.total_height + TOP_MARGIN,
                    text, size
                )
        self.total_height += (text_obj.height + BUTTON_MARGIN_H)
        self.elements.append(text_obj)

    def add_button(self, callback, button_w, button_h, color, text, size):
        x = self.x + RIGHT_MARGIN
        y = self.y + self.total_height + TOP_MARGIN
        self.elements.append(Button(x,y,button_w,button_h, callback, color, text, size))
        self.total_height += button_h + BUTTON_MARGIN_H
