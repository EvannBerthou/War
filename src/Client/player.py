import pygame
import math

DISTANCE_FROM_CENTER = 500

class Player(pygame.sprite.Sprite):
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

    def create_surface(self, color):
        self.sprite.fill(color)
        rotated = pygame.transform.rotate(self.sprite, self.angle)
        center = self.rect.center
        self.rect = rotated.get_rect()
        self.rect.center = center
        return rotated

    def create_selector(self, win_w, win_h, angle):
        selector_x, selector_y = self.get_position(win_w, win_h, angle, 0,0, DISTANCE_FROM_CENTER - 75)
        return (selector_x, selector_y)

    def __init__(self, win_w, win_h, angle, local, identifier, color):
        super().__init__()
        self.w, self.h = 100,50
        self.x, self.y = self.get_position(win_w, win_h, angle, self.w / 2, self.h / 2, DISTANCE_FROM_CENTER)

        self.sprite = self.load_sprite('player.png')
        self.rect = self.sprite.get_rect()
        self.rect.center = (self.x + self.w / 2, self.y + self.h / 2) #Set the rect center to the center of the rectangle

        self.angle = self.look_at_center(win_w / 2, win_h / 2)
        self.local = local
        self.image = self.create_surface(color)

        self.selector = self.create_selector(win_w, win_h, angle)
        self.selector_selected = False
        self.selector_radius = 20

        self.targeting = True
        self.targets = []

        self.identifier = identifier


    def draw_target(self, game):
        if self.targeting:
            for target in self.targets:
                pygame.draw.line(game.blitting_surface, (255,255,0),
                                (self.rect.center), (target.rect.center), 10)

    def is_selector_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
        distance_to_center = (mouse_pos[0] - self.selector[0])**2 + (mouse_pos[1] - self.selector[1])**2
        return distance_to_center < self.selector_radius**2

    def get_target_list(self):
        return "targets " + " ".join(target.identifier for target in self.targets)
