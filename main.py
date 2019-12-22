import pygame

from UI.Disclaimer import Disclaimer
from UI.MvpMenu import MvpMenu

FPS = 30

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()
# pygame.mixer.music.load('Assets\Music\menu1.wav')
# pygame.mixer.music.play(-1)

canvas = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
pygame.mouse.set_cursor((8, 8), (0, 0), (0,) * 8, (0,) * 8)

clock = pygame.time.Clock()
menu = MvpMenu(canvas)

ui_context = {'menu': menu, 'disclaimer': Disclaimer(canvas)}

graphical_ui = ui_context['disclaimer']
graphical_ui.load_ui_context(ui_context)

while True:
    clock.tick(FPS)
    graphical_ui.clean_canvas()
    graphical_ui.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            new_ui = graphical_ui.key_press(event.dict)
            if new_ui:
                if new_ui == 'EXIT':
                    exit(0)  # TODO Try to exit
                    continue
                graphical_ui = new_ui
                graphical_ui.load_ui_context(ui_context)
                graphical_ui.update()
        elif event.type == pygame.QUIT:
            exit(0)
    graphical_ui.draw_widgets()
    pygame.display.update()
