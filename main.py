import pygame

from UI.Disclaimer import Disclaimer
from UI.ExitConfirmation import ExitConfirmation
from UI.MvpMenu import MvpMenu

FPS = 30

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()
# pygame.mixer.music.load('Assets\Music\menu1.wav')
# pygame.mixer.music.play(-1)

exit_confirmation = None

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
            new_ui = graphical_ui.key_press(
                event.dict) if exit_confirmation is None else exit_confirmation.key_press(
                event.dict)
            if new_ui:
                if new_ui == 'EXIT':
                    exit_confirmation = ExitConfirmation(canvas)
                elif new_ui == 'CONTINUE':
                    exit_confirmation = None
                else:
                    graphical_ui = new_ui
                    graphical_ui.load_ui_context(ui_context)
                    graphical_ui.update()
                    exit_confirmation = None
        elif event.type == pygame.QUIT:
            exit(0)
    graphical_ui.draw_widgets()
    if exit_confirmation is not None:
        exit_confirmation.draw_widgets()
    pygame.display.update()
