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
            self.draw()

    def draw(self):
        self.win.fill((0,0,0))

        for p in self.players:
            p.draw(self)

        pygame.display.update()

game = Game(800,800)
game.run()
