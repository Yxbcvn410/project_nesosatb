import pygame
import pygame.gfxdraw

from Engine.Interface import AbstractUI
from Engine.Level import LevelRuntime, Level
from Engine.Media import Sprite
from Engine.MiniGame import MiniGameWrapper
from MiniGames.StubMinigame import StubMinigame
from UI.GameUI import GameUI

# colors
LEMON = (255, 248, 176)
ORANGE = (240, 184, 0)
DARK = (0, 0, 0, 0.9 * 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


class PlayerObject(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()


class Icon(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        # self.path = path


class Decor(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()


class Menu(AbstractUI, pygame.sprite.Sprite):
    def __init__(self, canvas):
        # working with canvas
        super().__init__(canvas)
        self.WIDTH = self.canvas.get_width()
        self.HEIGHT = self.canvas.get_height()

        # положение слотов для игр
        self.game_center = [(int(0.2 * self.WIDTH), self.HEIGHT // 4),
                            (int(0.5 * self.WIDTH), self.HEIGHT // 4),
                            (int(0.8 * self.WIDTH), self.HEIGHT // 4)]

        # пустые иконки
        self.red_circle = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self.blue_circle = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self.green_circle = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)

        # изображения
        self.empties = pygame.Surface((0, 0), pygame.SRCALPHA)
        self.darkie = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        # пятно света
        self.light_stain = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.gfxdraw.filled_circle(self.light_stain,
                                     self.WIDTH // 2, self.HEIGHT // 4,
                                     self.WIDTH // 10, ORANGE)
        pygame.gfxdraw.filled_circle(self.light_stain, self.WIDTH // 2, self.HEIGHT // 4,
                                     int(0.95 * self.WIDTH // 10), LEMON)

        # иконка заглушки
        self.stupid = pygame.image.load("Assets/Artwork/dumb.png").convert_alpha(self.canvas)
        self.stupid = pygame.transform.scale(self.stupid, (self.WIDTH // 6, self.HEIGHT // 6))

        # добавление фонарика
        self.source_light = pygame.image.load("Assets/Artwork/flashlight_orange.png").convert_alpha(self.canvas)
        self.source_light = pygame.transform.scale(self.source_light,
                                                   (self.WIDTH // 4, self.HEIGHT // 4))
        self.player = PlayerObject(image=self.source_light)
        self.player.rect.center = (self.WIDTH // 2,
                                   self.HEIGHT - self.player.image.get_height() // 2)
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)
        self.turning = 1

        # луч
        self.light_on = True
        self.ray = PlayerObject(image=self.light_stain)
        self.player_group.add(self.ray)

        # 3 слота для игр
        self.slots = [Decor(image=self.darkie)] * 3
        for i in range(3):
            pygame.gfxdraw.filled_circle(self.slots[i].image, self.game_center[i][0], self.game_center[i][1],
                                         self.player.image.get_width() // 2, DARK)

        self.slots_group = pygame.sprite.Group()
        self.slots_group.add(*self.slots)

        # дамб
        self.dumb = Icon(image=self.stupid)
        self.dumb.rect.center = (self.WIDTH // 2, self.HEIGHT // 4)
        self.game_list = [self.dumb] * 3

        # уровни
        level = Level(120)
        game = MiniGameWrapper()
        game.append_mini_game(StubMinigame(4, Sprite(pygame.image.load('Assets/Artwork/exp_1.png'))))
        level.load(game)
        level.metadata = {'music': 'Assets/Sound/Sabrepulse - Termination Shock.wav'}
        self.levels = [level] * 3

        # иконка
        self.n_icons = 0
        self.counting = 0
        self.icons = []

    def key_press(self, event):
        # прокрутка иконок

        # кнопки перемещения
        if event['key'] == pygame.K_h or event['key'] == pygame.K_LEFT or event['key'] == pygame.K_a:
            if self.turning != 2:
                self.turning += 1

        elif event['key'] == pygame.K_l or event['key'] == pygame.K_RIGHT or event['key'] == pygame.K_d:
            if self.turning != 0:
                self.turning -= 1

        # перехад на уровень
        if event['key'] == pygame.K_SPACE:
            runtime = LevelRuntime()
            runtime.load(self.levels[self.turning])
            runtime.play()
            game_ui = GameUI(self.canvas)
            game_ui.load_ui_context(self.views)
            game_ui.set_runtime(runtime)
            return game_ui

        # вкл/выкл фонарика
        if event['key'] == pygame.K_p:
            self.light_on = not self.light_on

        # выход
        if event['key'] == pygame.K_q or event['key'] == pygame.K_ESCAPE:
            exit(0)

    def update(self):
        if not self.light_on:
            self.ray.image = self.empties
        else:
            self.ray.image = self.light_stain

        if self.turning == 1:
            self.player.image = self.source_light
            self.ray.rect.center = (self.WIDTH // 2, self.HEIGHT // 2)
        elif self.turning == 2:
            self.player.image = pygame.transform.rotate(self.source_light, 30)
            self.ray.rect.center = (int(0.2 * self.WIDTH), self.ray.image.get_height() // 2)
        elif self.turning == 0:
            self.player.image = pygame.transform.rotate(self.source_light, -30)
            self.ray.rect.center = (int(0.8 * self.WIDTH), self.ray.image.get_height() // 2)

    def draw_widgets(self):
        self.clean_canvas()
        self.slots_group.draw(self.canvas)
        self.player_group.draw(self.canvas)

    def add_level(self, level):
        if "icon" not in level.metadata:
            level.metadata['icon'] = 'Assets/Artwork/dumb.png'
        self.n_icons += 1
        new_icon = pygame.image.load(level.metadata['icon']).convert_alpha(self.canvas)
        self.game_list[self.n_icons].image = new_icon
        self.game_list[self.n_icons].rect = new_icon.get_rect()
        self.levels.append(level)
