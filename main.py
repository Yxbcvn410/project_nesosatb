import pygame

from Engine.Level import LevelRuntime, FPS, Level
from UI.GameUI import GameUI
from MiniGames.StubMinigame import StubMinigame
from MiniGames.VetaMinigame import VetaMiniGame
from Engine.MiniGame import MiniGameWrapper
from Engine.Media import Sprite

pygame.init()

canvas = pygame.display.set_mode([1080, 720])
img = pygame.image.load('Assets/Artwork/exp_1.png')
img = pygame.transform.rotozoom(img, 0, 10)
img2 = pygame.image.load('Assets/Artwork/m_r1.png')
img2 = pygame.transform.rotozoom(img2, 0, 10)

clock = pygame.time.Clock()
runtime = LevelRuntime()
graphical_ui = GameUI(canvas, runtime)

game = MiniGameWrapper()

# game.append_mini_game(StubMinigame(16, Sprite(img2)))

game.append_mini_game(VetaMiniGame(5000))


level = Level(4, 120, None, graphical_ui)
level.load(game)
runtime.load(level)
runtime.play()

while True:
    clock.tick(FPS)
    graphical_ui.clean_canvas()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if graphical_ui.key_press(event.dict):
                pass  # TODO change GUI
        elif event.type == pygame.QUIT:
            exit(0)
    graphical_ui.update()
    graphical_ui.draw_widgets()
    pygame.display.update()
