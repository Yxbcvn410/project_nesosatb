import pygame

import Engine.MiniGame
from Engine.Media import Sprite


class StubMinigame(Engine.MiniGame.AbstractMiniGame):
    def configure(self, config_json):
        if 'sprite' in config_json:
            self.spr = Sprite(config_json['sprite'])
            self.spr.transform(center=(400, 300))

    def reset(self):
        pass

    def __init__(self, life_time, sprite=Sprite('Assets/Artwork/bullet.png'), base_color=(0, 0, 0)):
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
        self.spr.transform(opacity=(2 * (0.5 - abs(time['delta']))) ** 2.1,
                           scale=1 + (0.5 - abs(time['delta'])) ** 2.1 * (0.5 if time['beats'] == 0 else 0.2))
        return {'delta_health': 0, 'delta_score': 0}

    def draw(self, time: dict, canvas):
        self.spr.draw(canvas)

    def handle(self, event):
        return {'delta_health': -10, 'delta_score': (1 - (2 * abs(event['time']['delta'])) ** 0.3) * 30}
