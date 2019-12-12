from Engine.AbstractMinigame import *
import pygame
import sys
import math


class StubMinigame(AbstractMiniGame):
    def __init__(self, start_time, life_time, canvas):
        super().__init__(start_time, life_time, canvas)
        self.r = 0
        self.color = None

    def update(self, time: dict):
        if time['beats'] == 0:
            self.color = (255 - (0.5 - abs(time['delta'])) * 70, 255 - (0.5 - abs(time['delta'])) * 200, (0.5 - abs(time['delta'])) * 230)
        else:
            self.color = (255, 255, 0)
        self.r = (0.5 - abs(time['delta'])) ** 2.1 * (100 if time['beats'] == 0 else 30) + 100

    def draw(self, time: dict, graphical_ui):
        self.canvas.fill((0,0,0))
        pygame.draw.rect(self.canvas, self.color, (200 - self.r, 200 - self.r, 2 * self.r, 2 * self.r))
        pygame.display.update()

    def handle(self, event):
        sys.stdout.write(str(event) + '\n')
        sys.stdout.flush()
