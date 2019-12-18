from Engine.Interface import AbstractUI
from Engine.Level import LevelRuntime
import pygame


class GameUI(AbstractUI):
    def update(self):
        self.runtime.update()

    def __init__(self, canvas, runtime: LevelRuntime = None):
        super().__init__(canvas)
        self.runtime = runtime

    def key_press(self, key):
        if (key != 'p') or not self.runtime:
            self.runtime.key_pressed(key)
            return

        if self.runtime.paused:
            self.runtime.play()
        else:
            self.runtime.pause()

    def draw_widgets(self):
        self.runtime.draw()
        if self.runtime.paused:
            font = pygame.font.Font('Assets/Fonts/Patapon.ttf', 20)
            pause_text = font.render('Pause', 1, (255, 255, 255))
            self.canvas.blit(pause_text, (400, 300))
        pass  # TODO
