from Engine.Interface import AbstractUI
from Engine.Level import LevelRuntime
import pygame

WHITE = (255, 255, 255)
BLUE = (0, 0, 200)
GREEN = (0, 200, 0)


class GameUI(AbstractUI):
    def update(self):
        self.info = self.runtime.update()

    def __init__(self, canvas, runtime: LevelRuntime = None):
        self.views = None
        super().__init__(canvas)
        self.runtime = runtime
        self.control_keys = [pygame.K_p, pygame.K_q, pygame.K_s]
        self.info = None

    def key_press(self, event):
        if self.info['over']:
            if event['key'] == pygame.K_q:
                return self.views['old']
            else:
                return

        if not (event['key'] in self.control_keys) and (self.runtime is not None):
            self.info = self.runtime.key_pressed(event)
            return

        # Toggle pause
        if event['key'] == pygame.K_p:
            if self.info['pause']:
                self.runtime.play()
            else:
                self.runtime.pause()

        if event['key'] == pygame.K_q:
            exit(0)

    def draw_widgets(self):
        size = self.canvas.get_size()
        center = [a / 2 for a in self.canvas.get_size()]

        self.runtime.draw(self.canvas)
        font = pygame.font.Font('Assets/Fonts/Patapon.ttf', 40)
        sc_text = font.render('Score: {}'.format(self.info['stats']['global_score']), 1, WHITE)
        l_sc_text = font.render('Mini_game score: {}'.format(self.info['stats']['current_score']), 1, WHITE)
        self.canvas.blit(sc_text, (0, 0))
        self.canvas.blit(l_sc_text, (0, 40))
        pygame.draw.rect(self.canvas, GREEN,
                         [40, size[1] - 80, (size[0] - 80) * self.info['stats']['progress'], 40])
        pygame.draw.rect(self.canvas, WHITE, [40, size[1] - 80, size[0] - 80, 40], 5)
        if self.info['over']:
            pause_text = font.render('Game over. Press Q to quit.', 1, WHITE)
            self.canvas.blit(pause_text, pause_text.get_rect(center=center))
            return
        if self.runtime.paused:
            pause_text = font.render('Pause', 1, WHITE)
            self.canvas.blit(pause_text, pause_text.get_rect(center=center))
        pass  # TODO
