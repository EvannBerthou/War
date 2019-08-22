import pygame
from pygame.locals import *

from player import Player

class GAME_PHASE:
    CHOOSING  = 1,
    TARGETING = 2,
    DONE      = 3
    RESULT    = 4,

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

        self.game_phase = GAME_PHASE.CHOOSING

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                if event.type == MOUSEBUTTONDOWN:
                    self.on_clicked()

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

    def on_clicked(self):
        for p in self.players:
            if p.is_selector_clicked(pygame.mouse.get_pos()) and self.game_phase == GAME_PHASE.TARGETING:
                if p.local:
                    p.selector_selected = not p.selector_selected
                else:
                    if p in self.players[0].targets:
                        self.players[0].targets.remove(p)
                    else:
                        self.players[0].targets.append(p)

    def switch_state(self, phase):
        if phase == self.game_phase: return

        self.game_phase = phase
        for p in self.players: p.targeting = False
        if self.game_phase == GAME_PHASE.TARGETING:
            for p in self.players: p.targeting = True

game = Game(1200,800)
game.run()
