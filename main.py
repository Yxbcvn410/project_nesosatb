import pygame

from Engine.Level import LevelRuntime, FPS, Level
from UI.GameUI import GameUI
from UI.Menu1 import Menu
from MiniGames.StubMinigame import StubMinigame
from Engine.MiniGame import MiniGameWrapper
from Engine.Media import Sprite

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
graphical_ui = Menu(canvas)

game = MiniGameWrapper()
for i in range(8):
    game.append_mini_game(StubMinigame(1, Sprite(img)))
    game.append_mini_game(StubMinigame(1, Sprite(img2)))

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
