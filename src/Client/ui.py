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

        self.text = Text(self.x + self.w / 2, self.y + self.h / 2, (255,255,255),text, size, True)

    def draw(self,game):
        pygame.draw.rect(game.blitting_surface, self.color, (self.x,self.y,self.w,self.h))
        self.text.draw(game)

    def is_clicked(self, mouse_position):
        if self.rect.collidepoint(mouse_position): self.callback()

class Text:
    def __init__(self, x,y, color, text, size, center=False):
        self.x,self.y = x,y
        self.color = color

        self.font = pygame.font.SysFont("Arial", size)
        self.surface = self.font.render(text, 1, self.color)
        self.height = self.surface.get_height()

        if center:
            self.x -= self.surface.get_width() / 2
            self.y -= self.surface.get_height() / 2

    def draw(self, game):
        game.blitting_surface.blit(self.surface, (self.x, self.y))

    def set_text(self, text):
        self.surface = self.font.render(text, 1, self.color)

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
                    (255,255,255), text, size
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
        for btn in self.buttons: btn.is_clicked(mouse_position)

    def toggle(self):
        self.show = not self.show

class RequestPanel:
    def __init__(self, x,y,w,h):
        self.rect = pygame.Rect(x,y,w,h)
        self.options_list = None
        self.buttons = []
        self.tittle = Text(
                    self.rect.x + self.rect.w / 2,
                    self.rect.y + TOP_MARGIN + 20,
                    (0,0,0), "Request", 52, center = True)
        self.show = True

    def draw(self, game):
        if not self.show: return
        pygame.draw.rect(game.blitting_surface, (192,192,192), self.rect)
        [e.draw(game) for e in self.buttons + [self.tittle]]
