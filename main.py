import pygame, copy

from Engine.Level import LevelRuntime, FPS, Level
from Engine.Media import Sprite
from UI.GameUI import GameUI
from UI.Menu1 import Menu
from MiniGames.StubMinigame import StubMinigame
from Engine.MiniGame import MiniGameWrapper
from Engine.Interface import AnimationRuntime

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()

canvas = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
img = pygame.image.load('Assets/Artwork/exp_1.png')
img = pygame.transform.rotozoom(img, 0, 10)
img2 = pygame.image.load('Assets/Artwork/m_r1.png')
img2 = pygame.transform.rotozoom(img2, 0, 10)

clock = pygame.time.Clock()
runtime = LevelRuntime()
graphical_ui = GameUI(canvas)
graphical_ui.set_runtime(runtime)

game = MiniGameWrapper()
for i in range(4):
    game.append_mini_game(StubMinigame(1, Sprite(img)))
    game.append_mini_game(StubMinigame(1, Sprite(img2)))

level = Level(4, 120, None, graphical_ui)
level.load(game)
runtime.load(level)
runtime.play()

runtime = None
graphical_ui = Menu(canvas)

while True:
    clock.tick(FPS)
    graphical_ui.clean_canvas()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            new_ui = graphical_ui.key_press(event)
            if new_ui:
                old_runtime = copy.copy(runtime)
                runtime = new_ui[1]
                old_ui = copy.copy(graphical_ui)
                graphical_ui = new_ui[0]
                graphical_ui.load_views({'old': (old_ui, old_runtime)})
                graphical_ui.set_runtime(runtime)
                if runtime:
                    runtime.play()
        elif event.type == pygame.QUIT:
            exit(0)
    graphical_ui.update()
    graphical_ui.draw_widgets()
    pygame.display.update()
