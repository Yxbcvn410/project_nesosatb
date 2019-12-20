from math import pi, cos

import pygame

from Engine.Interface import AbstractUI
from Engine.Level import LevelRuntime
from Engine.Media import Sprite

WHITE = (255, 255, 255)
BLUE = (0, 0, 200)
GREEN = (0, 200, 0)
RED = (255, 30, 0)

MARGIN = 40
RADIUS = 50
HEART_MIN_R = 0.8
HEART_PEAK_T = 0.35


class GameUI(AbstractUI):
    def update(self):
        self.info = self.runtime.update()

    def __init__(self, canvas, runtime: LevelRuntime = None):
        self.views = None
        super().__init__(canvas)
        self.runtime = runtime
        self.control_keys = [pygame.K_p, pygame.K_ESCAPE, pygame.K_k, pygame.K_m]
        self.info = None
        self.display_settings_popup = False
        self.display_controls = True

        heart_image = pygame.image.load('Assets/Artwork/UI/Game/heart.png')
        heart_image = pygame.transform.scale(heart_image, (int(RADIUS * 2 * 0.8),) * 2)
        self.heart_sprite = Sprite(heart_image)
        self.heart_sprite.transform(center=(canvas.get_size()[0] - MARGIN - RADIUS, MARGIN + RADIUS))

    def key_press(self, event):
        if self.info['over']:
            if event['key'] == pygame.K_ESCAPE:
                return self.views['old']
            else:
                return

        if not (event['key'] in self.control_keys) and (self.runtime is not None):
            self.runtime.key_pressed(event)
            return

        # Toggle pause
        if event['key'] == pygame.K_p:
            if self.info['pause']:
                if not self.display_settings_popup:
                    self.runtime.play()
            else:
                self.runtime.pause()

        if event['key'] == pygame.K_ESCAPE:
            return self.views['old']

        if event['key'] == pygame.K_k:
            if self.info['pause']:
                if self.display_settings_popup:
                    self.display_settings_popup = False
                    self.runtime.play()
                else:
                    self.display_settings_popup = True
            if not self.info['pause']:
                self.runtime.pause()
                self.display_settings_popup = True

        if event['key'] == pygame.K_m:
            self.display_controls = not self.display_controls

    def draw_controls(self):
        size = self.canvas.get_size()

        # Количество очков в левом верхнем углу
        font = pygame.font.Font('Assets/Fonts/Patapon.ttf', MARGIN)
        sc_text = font.render('Score: {}'.format(self.info['stats']['global_score']), 1, WHITE)
        l_sc_text = font.render('Current mini-game score: {}'.format(self.info['stats']['current_score']), 1, WHITE)
        self.canvas.blit(sc_text, (0, 0))
        self.canvas.blit(l_sc_text, (0, 40))

        # Индикатор здоровья в правом верхнем углу
        if self.info['over']:  # Полоса здоровья становится белым кругом в конце игры
            pygame.draw.ellipse(self.canvas, WHITE, [size[0] - MARGIN - RADIUS * 2, MARGIN, RADIUS * 2, RADIUS * 2], 5)
        else:
            pygame.draw.arc(self.canvas, RED, [size[0] - MARGIN - RADIUS * 2, MARGIN, RADIUS * 2, RADIUS * 2], pi / 2,
                            pi / 2 + 2 * pi * self.info['stats']['health_info']['health'] /
                            self.info['stats']['health_info']['max'], 5)

        scale_arg = self.runtime.get_time_dict()['delta']  # Рисуем пульсирующее сердечко
        if not abs(scale_arg) > 0.5 * HEART_PEAK_T:
            scale_factor = ((cos(2 * pi * scale_arg / HEART_PEAK_T) * 0.5 + 1) * (1 - HEART_MIN_R) + HEART_MIN_R)
        else:
            scale_factor = HEART_MIN_R
        if self.info['over']:
            scale_factor = HEART_MIN_R
            if self.info['stats']['health_info']['health'] == 0:  # Здоровье на нуле - сердечко разбито :(
                heart_image = pygame.image.load('Assets/Artwork/UI/Game/heart_broken.png')
                heart_image = pygame.transform.scale(heart_image, (int(RADIUS * 2 * 0.8),) * 2)
                self.heart_sprite = Sprite(heart_image)
                self.heart_sprite.transform(center=(size[0] - MARGIN - RADIUS, MARGIN + RADIUS))

        self.heart_sprite.transform(scale=scale_factor)
        self.heart_sprite.draw(self.canvas)

        # Индикатор прогресса внизу экрана
        pointer_coords = MARGIN + (size[0] - MARGIN * 2) * self.info['stats']['progress'], size[1] - MARGIN
        pygame.draw.polygon(self.canvas, GREEN,
                            [(pointer_coords[0], pointer_coords[1] - 5),
                             (pointer_coords[0] - 20, pointer_coords[1] - 30),
                             (pointer_coords[0] + 20, pointer_coords[1] - 30)])
        pygame.draw.line(self.canvas, WHITE, (MARGIN, size[1] - MARGIN), (size[0] - MARGIN, size[1] - MARGIN), 5)
        waypts = self.runtime.level.get_waypoints()
        for wp in waypts:  # Нарисуем точки резкого изменения мини-игр
            pygame.draw.line(self.canvas, WHITE, [MARGIN + (size[0] - MARGIN * 2) * wp, size[1] - MARGIN + 20],
                             [MARGIN + (size[0] - 80) * wp, size[1] - MARGIN], 5)

    def draw_widgets(self):
        center = [a / 2 for a in self.canvas.get_size()]

        self.runtime.draw(self.canvas)

        if self.display_controls:
            self.draw_controls()

        font = pygame.font.Font('Assets/Fonts/Patapon.ttf', MARGIN)

        if self.info['over']:  # Нарисовать экран конца игры
            over_text = font.render('Game over. Press Esc to exit.', 1, WHITE)
            self.canvas.blit(over_text, over_text.get_rect(center=center))
            return
        if self.runtime.paused:
            if self.display_settings_popup:  # Всплывающее меню настроек
                pass  # TODO
            else:  # Игра стоит на паузе
                pause_text = font.render('Paused', 1, WHITE)
                info_text = font.render('K - settings, M - toggle show controls, Esc - quit', 1, WHITE)
                self.canvas.blit(pause_text, pause_text.get_rect(center=center))
                self.canvas.blit(info_text, (center[0] - info_text.get_size()[0] / 2, center[1] + 40))
