import pygame
from pygame.locals import *

class Game:
    def __init__(self, w,h):
        self.w,self.h = w,h
        self.win = pygame.display.set_mode((self.w,self.h))
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
        self.draw()

    def draw(self):
        self.win.fill((0,0,0))

        pygame.display.update()

game = Game(800,800)
game.run()
