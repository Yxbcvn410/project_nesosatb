import pygame
from Engine.LevelRuntime import *
from StubMinigame import *

pygame.init()
pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.KEYUP])
canvas = pygame.display.set_mode([800, 600])
clock = pygame.time.Clock()
ll = Level.Level(4, 120, None)
ll.add_mini_game(StubMinigame(0, 16))
rh = LevelRuntime()
rh.load(ll)
rh.play()

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            print('Key caught')  # FIXME press procession delay
            rh.key_pressed(event.key)
        elif event.type == pygame.QUIT:
            exit(0)
    result = rh.update()
    if result['over']:
        print('Level complete')
        exit(0)
