import pygame

from Engine.Media import Sprite
from Engine.MiniGame import *


class StubMinigame(AbstractMiniGame):
    def __init__(self, life_time, sprite, base_color=(0, 0, 0)):
        super().__init__(life_time)
        self.spr: Sprite = sprite
        sprite.transform(center=(400, 300))
        self.color = None
        self.base_color = base_color

    def update(self, time: dict):
        self.color = (255 - 2 * abs(time['delta']) * (255 - self.base_color[0]),
                      255 - 2 * abs(time['delta']) * (255 - self.base_color[1]),
                      255 - 2 * abs(time['delta']) * (255 - self.base_color[2]))
        self.spr.set_opacity((2 * (0.5 - abs(time['delta']))) ** 2.1)
        self.spr.transform(scale=10 + (0.5 - abs(time['delta'])) ** 2.1 * (5 if time['beats'] == 0 else 2))
        return {'delta_health': 0, 'delta_score': 0}

    def draw(self, time: dict, graphical_ui):
        self.spr.draw(graphical_ui.canvas)
        pygame.display.update()

    def handle(self, event):
        print(str(event) + '\n')
        return {'delta_health': 0, 'delta_score': 0}
