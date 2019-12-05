from Engine.AbstractMinigame import *
import pygame
import sys


class StubMinigame(AbstractMiniGame):
    def __init__(self, start_time, life_time, canvas):
        super().__init__(start_time, life_time, canvas)
        self.x = 30

    def update(self, time: dict):
        pass

    def draw(self, time: dict, graphical_ui):
        if time['bars'] < self.start_time:
            return
        if time['beat_type'] == 1:
            self.x += 10
        elif time['beat_type'] == 2:
            self.x -= 30
        self.canvas.fill((0,0,0))
        pygame.draw.rect(self.canvas, (255, 255, 0), (self.x, 0, 100, 100))
        pygame.display.update()

    def handle(self, event):
        sys.stdout.write(str(event) + '\n')
        sys.stdout.flush()
