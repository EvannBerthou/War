import pygame
from pygame.locals import *

from player import Player
from ui import StrategyChooser

class GAME_PHASE:
    CHOOSING  = 1,
    TARGETING = 2,
    DONE      = 3
    RESULT    = 4,

class Game:
    def create_strategy_chooser(self):
        strategy_chooser_w = 600
        strategy_chooser_h = 750
        strategy_chooser = StrategyChooser(
                                self.DESIGN_W / 2 - strategy_chooser_w / 2,
                                self.DESIGN_H / 2 - strategy_chooser_h / 2,
                                strategy_chooser_w,
                                strategy_chooser_h)

        FONT_SIZE = 84
        strategy_chooser.add_button(self.on_attack, 540, 300, (255,0,0), "Attack", FONT_SIZE)
        strategy_chooser.add_button(self.on_defence, 540, 300, (0,0,255), "Defend", FONT_SIZE)

        return strategy_chooser

    def __init__(self, w,h):
        self.w,self.h = w,h
        self.DESIGN_W, self.DESIGN_H = 1920,1080
        self.ratio = (self.DESIGN_W / self.w, self.DESIGN_H / self.h)
        self.blitting_surface = pygame.Surface((self.DESIGN_W, self.DESIGN_H))
        self.win = pygame.display.set_mode((self.w,self.h))
        self.running = True
        self.players = pygame.sprite.Group()
        self.number_of_player = 6
        default_rotation = -90

        for player in range(self.number_of_player):
            angle = player * (360 / self.number_of_player) - default_rotation
            self.players.add(Player(self.DESIGN_W, self.DESIGN_H, angle, local = player == 0))

        self.game_phase = GAME_PHASE.CHOOSING
        self.strategy_chooser = self.create_strategy_chooser()

    def run(self):
        while self.running:
            mouse_position = self.screen_to_world(pygame.mouse.get_pos())
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                if event.type == MOUSEBUTTONDOWN:
                    if self.game_phase == GAME_PHASE.CHOOSING: self.strategy_chooser.update(mouse_position)
                    else: self.on_clicked()

            self.draw()

    def draw(self):
        self.blitting_surface.fill((0,0,0))
        self.win.fill((0,0,0))

        #Draw circle
        pygame.draw.circle(self.blitting_surface, (255,255,255),
                          (self.DESIGN_W // 2, self.DESIGN_H // 2), 500, 2)

        #Draw player starting from local in order to draw selector line above other selector
        self.players.draw(self.blitting_surface)

        for p in self.players:
            p.draw_target(self)

        self.strategy_chooser.draw(self)

        self.win.blit(pygame.transform.scale(self.blitting_surface, (self.w,self.h)),(0,0))
        pygame.display.update()

    def on_clicked(self):
        mouse_position = self.screen_to_world(pygame.mouse.get_pos())
        for p in self.players:
            # if p.is_selector_clicked(mouse_position) and self.game_phase == GAME_PHASE.TARGETING:
            if p.is_selector_clicked(mouse_position):
                if p.local:
                    p.selector_selected = not p.selector_selected
                else:
                    player = self.players.sprites()[0]
                    if p in player.targets:
                        player.targets.remove(p)
                    else:
                        player.targets.append(p)

    def switch_state(self, phase):
        if phase == self.game_phase: return

        self.game_phase = phase
        for p in self.players: p.targeting = False
        if self.game_phase == GAME_PHASE.TARGETING:
            for p in self.players: p.targeting = True

    def on_attack(self):
        print('attack')

    def on_defence(self):
        print('defence')

    def screen_to_world(self, pos):
        return (int(pos[0] * self.ratio[0]), int(pos[1] * self.ratio[1]))

game = Game(1280, 720)
game.run()
