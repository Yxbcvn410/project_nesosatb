from Engine.Interface import AbstractUI
from Engine.Level import LevelRuntime
import pygame

WHITE = (255, 255, 255)


class GameUI(AbstractUI):
    def load_views(self, views):
        self.views = views

    def update(self):
        self.info = self.runtime.update()

    def __init__(self, canvas, runtime: LevelRuntime = None):
        self.views = None
        super().__init__(canvas)
        self.runtime = runtime
        self.control_keys = [pygame.K_p, pygame.K_q, pygame.K_s]
        self.info = None
        self.center = [a / 2 for a in self.canvas.get_size()]

    def key_press(self, event):
        if self.info['over']:
            return  # Goto

        if not (event.key in self.control_keys) and (self.runtime is not None):
            self.info = self.runtime.key_pressed(event)
            return

        # Toggle pause
        if event.key == pygame.K_p:
            if self.info['pause']:
                self.runtime.play()
            else:
                self.runtime.pause()

        if event.key == pygame.K_q:
            exit(0)

    def draw_widgets(self):
        self.runtime.draw()
        font = pygame.font.Font('Assets/Fonts/Patapon.ttf', 40)
        sc_text = font.render('Score: {}'.format(self.info['stats']['global_score']), 1, WHITE)
        l_sc_text = font.render('Mini_game score: {}'.format(self.info['stats']['current_score']), 1, WHITE)
        self.canvas.blit(sc_text, (0, 0))
        self.canvas.blit(l_sc_text, (0, 40))
        if self.info['over']:
            pause_text = font.render('Game over. Press Q to quit.', 1, WHITE)
            self.canvas.blit(pause_text, self.center)
            return
        if self.runtime.paused:
            pause_text = font.render('Pause', 1, WHITE)
            self.canvas.blit(pause_text, self.center)
        pass  # TODO
