import pygame
import pygame.gfxdraw

from Engine.Interface import AbstractUI
from Engine.Level import LevelRuntime, Level
from Engine.Media import Sprite
from Engine.MiniGame import MiniGameWrapper
from MiniGames.StubMinigame import StubMinigame
from MiniGames.VetaMinigame import VetaMiniGame
from UI.GameUI import GameUI

# colors
LEMON = (255, 248, 176)
ORANGE = (240, 184, 0)


class Menu(AbstractUI, pygame.sprite.Sprite):
    def __init__(self, canvas):
        super().__init__(canvas)
        # добавление фонарика
        self.player = pygame.sprite.Sprite()
        self.source_light = pygame.image.load("Assets/Artwork/flashlight_orange.png").convert_alpha(self.canvas)
        self.source_light = pygame.transform.scale(self.source_light,
                                                   (self.canvas.get_width() // 4, self.canvas.get_height() // 4))
        self.player.image = self.source_light
        self.player.rect = self.source_light.get_rect()
        self.player.rect.center = (self.canvas.get_width() // 2,
                                   self.canvas.get_height() - self.player.image.get_height() // 2)
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)
        self.turning = 1

        # луч
        self.light_on = True
        self.ray = pygame.sprite.Sprite()

        self.ray.image = pygame.Surface((self.canvas.get_width(), self.canvas.get_height()), pygame.SRCALPHA)
        pygame.gfxdraw.filled_circle(self.ray.image,
                                     self.canvas.get_width() // 2, self.canvas.get_height() // 4,
                                     self.player.image.get_width() // 2, ORANGE)
        pygame.gfxdraw.filled_circle(self.ray.image, self.canvas.get_width() // 2, self.canvas.get_height() // 4,
                                     int(0.74 * self.player.image.get_height()), LEMON)
        self.ray.rect = self.ray.image.get_rect()
        self.player_group.add(self.ray)

        # пустое место
        self.nothing = pygame.sprite.Sprite()
        self.nothing.image = pygame.image.load("Assets/Artwork/dumb.png").convert_alpha(self.canvas)
        self.nothing.image = pygame.transform.scale(self.nothing.image,
                                                    (self.canvas.get_width() // 6, self.canvas.get_height() // 6))
        pygame.gfxdraw.filled_circle(self.ray.image,
                                     self.canvas.get_width() // 2, self.canvas.get_height() // 4, 0, (0, 0, 0))
        self.nothing.rect = self.nothing.image.get_rect()
        self.nothing.rect.center = (self.canvas.get_width() // 2, self.canvas.get_height() // 4)
        self.game_list = [self.nothing] * 3
        self.n_icons = 0
        self.icon_group = pygame.sprite.Group()
        self.icon_group.add(*self.game_list)

        # уровни
        level = Level(120)
        game = MiniGameWrapper()
        game.append_mini_game(
            StubMinigame(4, Sprite(pygame.transform.rotozoom(pygame.image.load('Assets/Artwork/exp_1.png'), 0, 10))))
        game.append_mini_game(VetaMiniGame(4))
        level.load(game)
        self.levels = [level] * 3

    def key_press(self, event):
        if event['key'] == pygame.K_q or event['key'] == pygame.K_ESCAPE:
            exit(0)
        if event['key'] == pygame.K_h or event['key'] == pygame.K_LEFT or event['key'] == pygame.K_a:
            self.turning += 1
            self.turning = self.turning % 3

        elif event['key'] == pygame.K_l or event['key'] == pygame.K_RIGHT or event['key'] == pygame.K_d:
            self.turning -= 1
            self.turning = self.turning % 3

        if event['key'] == pygame.K_SPACE:
            runtime = LevelRuntime()
            self.levels[self.turning].reset()
            runtime.load(self.levels[self.turning])
            game_ui = GameUI(self.canvas)
            game_ui.set_runtime(runtime)
            runtime.play()
            return game_ui

    def update(self):
        if self.turning == 2:
            self.player.image = self.source_light
            self.ray.rect.center = (self.canvas.get_width() // 2, self.canvas.get_height() // 2)
        elif self.turning == 0:
            self.player.image = pygame.transform.rotate(self.source_light, 30)
            self.ray.rect.center = (int(0.2 * self.canvas.get_width()), self.ray.image.get_height() // 2)
        elif self.turning == 1:
            self.player.image = pygame.transform.rotate(self.source_light, -30)
            self.ray.rect.center = (int(0.8 * self.canvas.get_width()), self.ray.image.get_height() // 2)

    def draw_widgets(self):
        self.clean_canvas()
        self.player_group.draw(self.canvas)
        self.icon_group.draw(self.canvas)

    def add_level(self, level):
        if "icon" not in level.metadata:
            level.metadata['icon'] = self.nothing.image

        new_icon = pygame.image.load(level.metadata['icon']).convert_alpha(self.canvas)
        self.game_list[self.n_icons].image = new_icon
        self.game_list[self.n_icons].rect = new_icon.get_rect()
        self.games.append(level.game)
