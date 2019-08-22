import pygame
from pygame.locals import *

from player import Player

class Game:
    def __init__(self, w,h):
        self.w,self.h = w,h
        self.win = pygame.display.set_mode((self.w,self.h))
        self.running = True
        self.players = []
        self.number_of_player = 6
        default_rotation = -90

        for player in range(self.number_of_player):
            angle = player * (360 / self.number_of_player) - default_rotation
            self.players.append(Player(self.w, self.h, angle, local = player == 0))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                if event.type == MOUSEBUTTONDOWN:
                    for p in self.players:
                        if p.is_selector_clicked(pygame.mouse.get_pos()):
                            if p.local:
                                p.selector_selected = not p.selector_selected
                            else:
                                if p in self.players[0].targets:
                                    self.players[0].targets.remove(p)
                                else:
                                    self.players[0].targets.append(p)

            self.draw()
            self.update()

    def draw(self):
        self.win.fill((0,0,0))

        #Draw player starting from local to draw selector line above other selector
        for p in self.players[::-1]:
            p.draw(self)

        pygame.display.update()

    def update(self):
        pass

game = Game(800,800)
game.run()
