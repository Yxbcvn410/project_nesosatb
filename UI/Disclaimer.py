import enum
import time

import pygame

from Engine.Interface import AnimationRuntime, AbstractUI
from Engine.Media import Sprite


class Status(enum.Enum):
    TRIANGLE = 0
    PRESENT = 1
    AWAIT = 2


class Disclaimer(AbstractUI):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.runtime = AnimationRuntime()
        self.status = Status.TRIANGLE

    def schedule_animations(self):
        center = tuple(a / 2 for a in self.canvas.get_size())
        pygame_logo = Sprite('Assets/Artwork/UI/Disclaimer/pygame_logo.png')
        pygame_logo.transform(center=center, opacity=0)
        noblow_logo = Sprite('Assets/Artwork/UI/Disclaimer/noblow_logo.png')
        noblow_logo.transform(center=center, opacity=0)
        times_font = pygame.font.Font('Assets/Fonts/Times New Roman.ttf', 30)
        greet_sprite = Sprite(times_font.render('From creators of lab3.1 and lab3.2', 1, (255,) * 3))
        greet_sprite.transform(center=center, opacity=0)

        self.runtime.add_animation_by_keyframes(pygame_logo, {
            2: {},
            4: {'opacity': 1, 'scale': 1.2},
            6: {'opacity': 0, 'scale': 1.4}
        })
        self.runtime.add_animation_by_keyframes(noblow_logo, {
            7: {},
            9: {'opacity': 1, 'scale': 1.2},
            11: {'opacity': 0, 'scale': 1.4}
        })
        self.runtime.add_animation_by_keyframes(greet_sprite, {
            12: {},
            14: {'opacity': 1, 'scale': 1.2},
            16: {'opacity': 0, 'scale': 1.4},
            17: {}
        })

    def key_press(self, event):
        if self.status == Status.TRIANGLE:
            if event['key'] == pygame.K_ESCAPE:
                return 'EXIT'
            self.status = Status.PRESENT
            self.schedule_animations()
        else:
            self.runtime.delete_all_animations()
            return self.views['menu']

    def update(self):
        self.runtime.update_all(self.canvas)
        if self.status == Status.PRESENT and not self.runtime.is_animating():
            self.status = Status.AWAIT
        if self.status == Status.AWAIT and not self.runtime.is_animating():
            center = tuple(a / 2 for a in self.canvas.get_size())
            times_font = pygame.font.Font('Assets/Fonts/Times New Roman.ttf', 30)
            continue_sprite = Sprite(times_font.render('Press any key to continue', 1, (255,) * 3))
            continue_sprite.transform(center=center, opacity=0)
            self.runtime.add_animation_by_keyframes(continue_sprite, {
                1: {'opacity': 1},
                2: {'opacity': 0}
            })

    def draw_widgets(self):
        if self.status == Status.TRIANGLE:
            delta = (time.time() % 0.5 - 0.25) * 2
            r = (0.5 - abs(delta)) ** 2.1 * 50 + 100
            pygame.draw.ellipse(self.canvas, (0, 255, 255), (400 - r, 400 - r, r * 2, r * 2))
