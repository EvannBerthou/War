import pygame
import math

DISTANCE_FROM_CENTER = 300

class Player:
    def get_position(self, win_w, win_y, angle, rect_w, rect_h, dist):
        angle_x = round(math.cos(math.radians(angle)) * dist + win_w / 2 - rect_w)
        angle_y = round(math.sin(math.radians(angle)) * dist + win_y / 2 - rect_h)
        return angle_x, angle_y

    def look_at_center(self, center_w, center_h):
        delta_x, delta_y = center_w - (self.x + self.w / 2), center_h - (self.y + self.h / 2)
        angle = math.atan2(delta_x, delta_y)
        return math.degrees(angle)

    def load_sprite(self, file_path):
        return pygame.transform.scale(
                pygame.image.load(file_path),
                (self.w, self.h))

    def create_surface(self):
        rotated = pygame.transform.rotate(self.sprite, self.angle)
        center = self.rect.center
        self.rect = rotated.get_rect()
        self.rect.center = center
        return rotated

    def create_selector(self, win_w, win_h, angle):
        selector_x, selector_y = self.get_position(win_w, win_h, angle, 0,0, DISTANCE_FROM_CENTER - 75)
        return (selector_x, selector_y)

    def __init__(self, win_w, win_h, angle, local):
        self.w, self.h = 100,50
        self.x, self.y = self.get_position(win_w, win_h, angle, self.w / 2, self.h / 2, DISTANCE_FROM_CENTER)
        self.angle = self.look_at_center(win_w / 2, win_h / 2)
        self.sprite = self.load_sprite('player.png')
        self.rect = self.sprite.get_rect()
        self.rect.center = (self.x + self.w / 2, self.y + self.h / 2) #Set the rect center to the center of the rectangle
        self.surface = self.create_surface()

        self.local = local
        self.selector = self.create_selector(win_w, win_h, angle)
        self.selector_color = (255,0,0) if self.local else (255,0,255)


    def draw(self, game):
        pygame.draw.circle(game.win, (255,255,255), (game.w // 2, game.h // 2), DISTANCE_FROM_CENTER, 2)
        game.win.blit(self.surface, self.rect)
        # pygame.draw.rect(game.win, (255,0,0), (self.x, self.y, self.w, self.h))

        pygame.draw.circle(game.win, self.selector_color, (self.selector[0], self.selector[1]), 20)
