import pygame
import sys
from os import path
import math
from Engine.MiniGame import AbstractMiniGame
from Engine.Media import Sprite


class VetaMinigame(AbstractMiniGame):
    def __init__(self, life_time):
        super().__init__(life_time)
        self.r = 0
        self.color = None
        img_dir = path.join(path.dirname(__file__), '../Assets/Artwork/img')
        background = pygame.image.load(path.join(img_dir, 'background01.png')).convert()
        background = pygame.transform.rotozoom(background, 0, 1.4)
        self.backgrounds = [Sprite(background), Sprite(background)]
        self.dx = 0
        bird = pygame.image.load(path.join(img_dir, 'bird.png')).convert()
        bird = pygame.transform.rotozoom(bird, 0, 0.2)
        self.bird = Sprite(bird)

    def update(self, time: dict):
        self.dx = 100 * (4 * time['bars'] + time['beats'] + time['delta'])
        if self.dx >= self.backgrounds[0].image.get_size()[0]:
            self.dx -= self.backgrounds[0].image.get_size()[0]
        return {'delta_health': 0, 'delta_score': 0}

    def draw(self, time: dict, graphical_ui):
        background_rect = [a / 2 for a in graphical_ui.canvas.get_size()]
        self.backgrounds[0].transform(center=(background_rect))
        self.backgrounds[1].transform(center=(background_rect))
        # self.bird.transform(())
        self.backgrounds[0].transform_relative(move=(- self.dx, 0))
        x = self.backgrounds[0].image.get_size()[0]
        self.backgrounds[1].transform_relative(move=(x - self.dx, 0))
        self.backgrounds[0].draw(graphical_ui.canvas)
        self.backgrounds[1].draw(graphical_ui.canvas)
        self.bird.draw(graphical_ui.canvas)

    def handle(self, event):
        sys.stdout.write(str(event) + '\n')
        sys.stdout.flush()
        return {'delta_health': 0, 'delta_score': 0}

