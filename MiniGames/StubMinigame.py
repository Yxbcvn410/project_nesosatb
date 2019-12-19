import pygame

from Engine.Media import Sprite, MusicPlayer
from Engine.MiniGame import *


class StubMinigame(AbstractMiniGame):
    def __init__(self, life_time, sprite, base_color=(0, 0, 0)):
        super().__init__(life_time)
        self.spr: Sprite = sprite
        sprite.transform(center=(400, 300))
        self.color = None
        self.base_color = base_color
        self.bp = pygame.mixer.Sound('Assets/Sound/wrong.wav')

    def update(self, time: dict):
        self.color = (255 - 2 * abs(time['delta']) * (255 - self.base_color[0]),
                      255 - 2 * abs(time['delta']) * (255 - self.base_color[1]),
                      255 - 2 * abs(time['delta']) * (255 - self.base_color[2]))
        self.spr.set_opacity((2 * (0.5 - abs(time['delta']))) ** 2.1)
        self.spr.transform(scale=1 + (0.5 - abs(time['delta'])) ** 2.1 * (0.5 if time['beats'] == 0 else 0.2))
        return {'delta_health': 0, 'delta_score': 0}

    def draw(self, time: dict, graphical_ui):
        if time['beat_type'] in (1, 2):
            self.bp.play()
        self.spr.draw(graphical_ui.canvas)

    def handle(self, event):
        print(str(event) + '\n')
        self.bp.play()
        return {'delta_health': 0, 'delta_score': (1 - (2 * abs(event['time']['delta'])) ** 0.3) * 30}
