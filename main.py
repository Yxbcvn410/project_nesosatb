import pygame

from Engine.LevelRuntime import LevelRuntime, FPS
from Engine.Level import Level
from Engine.GameUI import GameUI
from StubMinigame import StubMinigame

pygame.init()
pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.KEYUP])
canvas = pygame.display.set_mode([800, 600])
clock = pygame.time.Clock()
level = Level(4, 120, None)
level.add_mini_game(StubMinigame(0, 16, canvas ))
graphical_ui = GameUI(canvas)
runtime = LevelRuntime(graphical_ui)
runtime.load(level)
runtime.play()

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            runtime.key_pressed(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            graphical_ui.mouse_click(event.pos)
        elif event.type == pygame.QUIT:
            exit(0)
    result = runtime.update()
    if result['over']:
        print('Level complete')
        exit(0)
