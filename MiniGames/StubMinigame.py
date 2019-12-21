import pygame

import Engine.MiniGame
from Engine.Media import Sprite


class StubMinigame(Engine.MiniGame.AbstractMiniGame):
    def reset(self):
        pass

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

    def draw(self, time: dict, canvas):
        if time['beat_type'] in (1, 2):
            self.bp.play()
        self.spr.draw(canvas)

    def handle(self, event):
        return {'delta_health': -50, 'delta_score': (1 - (2 * abs(event['time']['delta'])) ** 0.3) * 30}
