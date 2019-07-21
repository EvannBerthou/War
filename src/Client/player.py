import pygame
import math

DISTANCE_FROM_CENTER = 300

class Player:
    def get_position(self, win_w, win_y, angle, rect_w, rect_h):
        angle_x = round(math.cos(math.radians(angle)) * DISTANCE_FROM_CENTER + win_w / 2 - rect_w / 2)
        angle_y = round(math.sin(math.radians(angle)) * DISTANCE_FROM_CENTER + win_y / 2 - rect_h / 2)
        return angle_x, angle_y

    def __init__(self, win_w, win_y, angle):
        self.w, self.h = 100,50
        self.x, self.y = self.get_position(win_w, win_y, angle, self.w, self.h)

    def draw(self, game):
        pygame.draw.rect(game.win, (255,255,255), (self.x, self.y, self.w, self.h))
