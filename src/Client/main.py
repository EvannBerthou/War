import socket
import json
import pygame
from pygame.locals import *

from player import Player
from ui import StrategyChooser, Button, Text, RequestPanel
from Client import GameSocket

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
        strategy_chooser.add_button(self.on_defense, 540, 300, (0,0,255), "Defend", FONT_SIZE)

        return strategy_chooser

    def create_request_panel(self):
        request_panel_w = 600
        request_panel_h = 500
        request_panel = RequestPanel(
                                self.DESIGN_W - request_panel_w,
                                self.DESIGN_H - request_panel_h,
                                request_panel_w,
                                request_panel_h)

        return request_panel

    def __init__(self, w,h):
        self.w,self.h = w,h
        self.DESIGN_W, self.DESIGN_H = 1920,1080
        self.ratio = (self.DESIGN_W / self.w, self.DESIGN_H / self.h)
        self.blitting_surface = pygame.Surface((self.DESIGN_W, self.DESIGN_H))
        self.win = pygame.display.set_mode((self.w,self.h))
        self.running = True

        self.game_socket = GameSocket(self)

        self.players = pygame.sprite.Group()
        self.number_of_player = 0

        self.game_phase = GAME_PHASE.CHOOSING
        self.strategy_chooser = self.create_strategy_chooser()
        self.request_panel = self.create_request_panel()

        self.confirm_button = Button(0,0,150,40, self.confirm, (150,150,150), 'Confirm', 36)

        self.scores = {}
        self.scores_texts = {}

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

        self.game_socket.close()

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

        for text in self.scores_texts:
            self.scores_texts[text].draw(self)

        if self.game_phase == GAME_PHASE.CHOOSING:
            self.strategy_chooser.draw(self)

        if self.game_phase == GAME_PHASE.TARGETING:
            self.confirm_button.draw(self)

        self.request_panel.draw(self)

        self.win.blit(pygame.transform.scale(self.blitting_surface, (self.w,self.h)),(0,0))
        pygame.display.update()

    def on_clicked(self):
        mouse_position = self.screen_to_world(pygame.mouse.get_pos())
        for p in self.players:
            if p.is_selector_clicked(mouse_position) and self.game_phase == GAME_PHASE.TARGETING:
                if p.local:
                    p.selector_selected = not p.selector_selected
                else:
                    player = self.players.sprites()[0]
                    print(p.identifier)
                    if p in player.targets:
                        player.targets.remove(p)
                    else:
                        player.targets.append(p)

        if self.game_phase == GAME_PHASE.TARGETING:
            self.confirm_button.is_clicked(mouse_position)

    def switch_state(self, phase):
        if phase == self.game_phase: return

        self.game_phase = phase
        for p in self.players: p.targeting = False
        if self.game_phase == GAME_PHASE.TARGETING:
            for p in self.players: p.targeting = True

    def on_attack(self):
        self.game_phase = GAME_PHASE.TARGETING
        self.strategy_chooser.toggle()

    def on_defense(self):
        self.game_phase = GAME_PHASE.DONE
        self.game_socket.socket.send('defense'.encode())
        self.strategy_chooser.toggle()

    def confirm(self):
        self.game_phase = GAME_PHASE.DONE
        self.game_socket.socket.send(self.local_player.get_target_list().encode())
        print('Done')

    def screen_to_world(self, pos):
        return (int(pos[0] * self.ratio[0]), int(pos[1] * self.ratio[1]))

    def add_player(self, clients):
        self.players.empty()
        self.scores_texts = {}
        self.number_of_player = len(clients)

        default_rotation = -90

        for i,client in enumerate(clients):
            parts = client.split(':')
            if int(parts[1]) == self.game_socket.port:
                identifier = '{}:{}'.format(parts[0], parts[1])
                color = self.convert_to_color(parts[2])
                self.local_player = Player(self.DESIGN_W, self.DESIGN_H, -default_rotation, 1, client, color)
                self.players.add(self.local_player)
                self.scores_texts[identifier] = Text(0,0, color, "0", 46)
                clients.remove(client)


        for i,client in enumerate(clients):
            parts = client.split(':')
            identifier = '{}:{}'.format(parts[0], parts[1])
            port = int(parts[1])
            color = self.convert_to_color(parts[2])
            local = port == self.game_socket.port
            angle = (i + 1) * (360 / self.number_of_player) - default_rotation
            self.players.add(Player(self.DESIGN_W, self.DESIGN_H, angle, local, client, color))
            self.scores_texts[identifier] = Text(0,(i + 1) * 50, color, "0", 46)

    def set_scores(self, str_data):
        self.scores = json.loads(str_data)
        for key in self.scores_texts:
            text = self.scores_texts[key]
            score = self.scores[key]
            text.set_text(str(score))

    def set_local_color(self, r,g,b):
        self.players.sprites()[0].set_color((r,g,b))

    def convert_to_color(self, string):
        return [int(part) for part in string.split(',')]


game = Game(1280, 720)
game.run()
