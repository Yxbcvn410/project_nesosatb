import math
from os import path, listdir
from random import choice

import pygame

from Engine.Media import Sprite
from Engine.MiniGame import AbstractMiniGame

img_dir = path.join(path.dirname(__file__), '../Assets/Artwork/img/HillMiniGame/')
raccoon_dir = path.join(path.dirname(__file__), '../Assets/Artwork/img/HillMiniGame/raccoon/')


class Raccoon:
    def __init__(self):
        self.sprites = {'run': self.get_sprites(self.get_pathes(raccoon_dir + 'run')),
                        'jump': self.get_sprites(self.get_pathes(raccoon_dir + 'jump')),
                        'death': self.get_sprites(self.get_pathes(raccoon_dir + 'ko'))}
        self.counters = {'run': 0, 'jump': 0, 'death': 0}
        self.state = 'run'
        self.x = 0
        self.y = 0

    def draw(self, key, canvas):
        if key == 'jump' and self.counters[key] >= len(self.sprites[key]):
            self.counters[key] = 0
            self.y = canvas.get_height() * 0.6
            self.state = 'run'
        elif self.counters[key] >= len(self.sprites[key]) and key != 'death':
            self.counters[key] = 0
        elif key == 'death' and self.counters[key] >= len(self.sprites[key]):
            self.counters[key] = len(self.sprites[key]) - 1

        self.sprites[key][int(self.counters[key])].transform(center=[self.x, self.y], scale=0.5)
        self.sprites[key][int(self.counters[key])].draw(canvas)

    def get_pathes(self, directory):
        if directory.endswith('/'):
            directory = directory[:-1]
        return [directory + '/' + file for file in listdir(directory) if '.png' in file]

    def get_sprites(self, pathes):
        images = [[pygame.image.load(patth).convert_alpha(), patth[-6:-4]] for patth in pathes]
        sprites = [0] * len(images)
        for image in images:
            if image[1][0] == 0:
                number = int(image[1][1]) - 1
            else:
                number = int(image[1]) - 1
            sprites[number] = Sprite(image[0])
        return sprites


class Rock:
    def __init__(self, time):
        self.sprite = Sprite(pygame.image.load(choice(
            [img_dir + 'rocks/' + file for file in listdir(img_dir + 'rocks')])))
        self.hill_alpha = 0.26
        self.position = None
        self.angle = 0
        self.time = time

    def draw(self, canvas):
        if self.position is None:
            x = 1.1 * canvas.get_width()
            y = - 0.6 * canvas.get_width() * self.hill_alpha / 2 + canvas.get_height() / 2 - 140
            self.sprite.transform(center=(x, y))
            self.position = [x, y]
        self.sprite.transform(angle=self.angle)
        self.sprite.transform(center=self.position)
        self.sprite.draw(canvas)

    def update(self):
        if self.position:

            self.angle += 10

            self.position[0] -= 10
            self.position[1] += 10 * self.hill_alpha




class HillMinigame(AbstractMiniGame):
    def configure(self, config_json):
        self.hill_image = Sprite(pygame.image.load(path.join(img_dir, config_json['hill'])).convert_alpha())
        self.background = Sprite(pygame.image.load(path.join(img_dir, config_json["background"])).convert())
        self.rocks = [Rock(time) for time in config_json['rock_times']]

    def reset(self):
        pass

    def __init__(self, life_time):
        super().__init__(life_time)
        self.hill_image = None
        self.background = None
        self.raccoon = Raccoon()
        self.rocks = None
        self.last_pressed = []

    def update(self, time: dict):
        self.raccoon.counters[self.raccoon.state] += 0.5
        if self.raccoon.state == 'jump':
            if self.raccoon.counters['jump'] < len(self.raccoon.sprites['jump'])/2:
                self.raccoon.y -= 20
            elif self.raccoon.counters['jump'] > len(self.raccoon.sprites['jump'])/2:
                self.raccoon.y += 20

        for rock in self.rocks:
            if rock.position and ((self.raccoon.x - rock.position[0]) ** 2 +
                                  (self.raccoon.y - rock.position[1]) ** 2) ** 0.5 < 100:
                self.raccoon.state = 'death'

        delta_health = 0
        if self.raccoon.state == 'death':
            delta_health = - 2

        for rock in self.rocks:
            if rock.time <= time['bars']:
                rock.update()

        return {'delta_health': delta_health, 'delta_score': 0}

    def draw(self, time: dict, canvas):
        background_rect = [a / 2 for a in canvas.get_size()]
        if self.raccoon.x == 0:
            self.raccoon.x = canvas.get_width() / 4
            self.raccoon.y = canvas.get_height() * 0.6
        self.hill_image.transform(center=background_rect)
        self.background.transform(center=background_rect)

        self.background.draw(canvas)
        self.hill_image.draw(canvas)

        self.raccoon.draw(self.raccoon.state, canvas)

        for rock in self.rocks:
            if rock.time <= time['bars']:
                rock.draw(canvas)

    def handle(self, event):
        if event['key']['unicode'] in ('w', 'a', 's', 'd') and math.fabs(event['time']['delta']) < 0.5:
            self.last_pressed.append(event['key']['unicode'])

        if self.last_pressed[-3:] == ['a', 's', 'd']:
            self.raccoon.state = 'jump'
            self.last_pressed = []
        return {'delta_health': 0, 'delta_score': 0}
