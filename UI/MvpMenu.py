import pygame

from Engine.Interface import AbstractUI
from Engine.Level import LevelRuntime
from Engine.LevelLoader import LevelLoader
from UI.GameUI import GameUI

FONT_SZ = 40
LINE_SZ = 50
MARGIN = 40

WHITE = (255, 255, 255)


class MvpMenu(AbstractUI):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.loader = LevelLoader()
        self.loader.scan_directory("Assets/Levels")
        self.levels = self.loader.get_levels_metadata()
        self.levels_id = list(self.levels.keys())
        self.level_pointer = 0
        self.first_in_view = 0
        self.lines_no = (self.canvas.get_size()[1] - MARGIN * 2) // LINE_SZ
        self.sound_playing = False

    def key_press(self, event):
        if event['key'] == pygame.K_KP_ENTER or event['key'] == pygame.K_SPACE:
            self.sound_playing = False
            pygame.mixer.music.stop()
            pygame.mixer.music.pause()

            level = self.loader.load_level(self.levels_id[self.level_pointer])
            runtime = LevelRuntime()
            runtime.load(level)
            runtime.play()
            gui = GameUI(self.canvas)
            gui.load_ui_context(self.views)
            gui.set_runtime(runtime)
            return gui

        if event['key'] == pygame.K_ESCAPE:
            return 'EXIT'

        if event['key'] == pygame.K_DOWN:
            self.level_pointer += 1
            if self.level_pointer >= len(self.levels):
                self.level_pointer -= 1
            if self.level_pointer > self.first_in_view + self.lines_no:
                self.first_in_view += 1

        if event['key'] == pygame.K_UP:
            self.level_pointer -= 1
            if self.level_pointer < 0:
                self.level_pointer += 1
            if self.level_pointer < self.first_in_view:
                self.first_in_view -= 1

    def update(self):
        if not self.sound_playing:
            self.sound_playing = True
            pygame.mixer.music.load('Assets/Music/menu1.wav')
            pygame.mixer.music.play(-1)

    def draw_widgets(self):
        font = pygame.font.Font("Assets/Fonts/Patapon.ttf", FONT_SZ)
        size = self.canvas.get_size()
        for i in range(self.lines_no):
            if i + self.first_in_view >= len(self.levels):
                continue
            level_id = self.levels_id[i + self.first_in_view]
            name = self.levels[level_id].get('name', '<id {}>'.format(level_id))
            level_text = font.render(name, 1, WHITE)
            self.canvas.blit(level_text, (MARGIN * 2, MARGIN + i * LINE_SZ + (LINE_SZ - FONT_SZ) // 2))
            if level_id == self.levels_id[self.level_pointer]:
                pygame.draw.rect(self.canvas, WHITE, [5, MARGIN + i * LINE_SZ, size[0] - 10, LINE_SZ], 5)
