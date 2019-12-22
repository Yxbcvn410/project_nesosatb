import math
from os import path
from random import randint as rnd

import pygame

from Engine.Media import Sprite
from Engine.MiniGame import AbstractMiniGame

# kinda of flappy bird
# with gaussianinan distribution for holes where bird loses health but the game continues
# movement can be down or up with those or also w, s characters
# how big velocity you get after click is determined with how near the beat the event it was

img_dir = path.join(path.dirname(__file__), '../Assets/Artwork/img')
speed = 250  # pixels per delta time


class Hole:
    def __init__(self, sigma, bk_height, d_height, is_up):
        self.sigma = sigma
        self.points_delta = 5
        self.points = []
        self.bk_height = bk_height
        self.d_height = d_height
        self.should_be_destroyed = False
        self.is_up = is_up
        self.dx = 0

        self.make_points()

    def make_points(self):
        number_of_points = (self.sigma * 6) // self.points_delta
        for i in range(number_of_points):
            y = math.exp(-(((i * self.points_delta - 3 * self.sigma) ** 2) / (2 * self.sigma ** 2)))
            self.points.append([i * self.points_delta, int(y * self.points_delta * self.sigma + self.d_height)])

    def get_y(self, x):
        return self.points[x // self.points_delta][1]

    def get_x(self, y):
        return int((2 * self.sigma ** 2 * math.log(y)) ** 0.5)

    def get_points(self, dx, width):
        moved_points = []

        # counting only for on_screen part of distribution
        if dx < self.sigma * 6:
            counter = dx // self.points_delta
        else:
            counter = (self.sigma * 6) // self.points_delta

        # counting points
        for i in range(counter):
            point = self.points[i]
            if self.is_up:
                moved_points.append([point[0] - dx + width, self.bk_height - point[1] + 2 * self.d_height])
            else:
                moved_points.append([point[0] - dx + width, point[1]])

        if moved_points[-1][0] < self.points_delta:
            self.should_be_destroyed = True

        # making polygon up to the edge
        if self.is_up:
            moved_points.append([moved_points[-1][0], self.bk_height + self.d_height])
            moved_points.append([width - dx, self.bk_height + self.d_height])
        else:
            moved_points.append([moved_points[-1][0], 0])
            moved_points.append([width - dx, 0])

        return moved_points


class Bird:
    def __init__(self):
        bird_up = pygame.image.load(path.join(img_dir, 'rose_up.png')).convert_alpha()
        bird_up = pygame.transform.rotozoom(bird_up, 0, 0.2)
        bird_down = pygame.image.load(path.join(img_dir, 'rose_down.png')).convert_alpha()
        bird_down = pygame.transform.rotozoom(bird_down, 0, 0.2)
        self.birds = [Sprite(bird_up), Sprite(bird_down)]
        self.up_or_down_bird = 0
        self.y = 0
        self.vy = 0

    def change_bird(self):
        self.up_or_down_bird += 1
        self.up_or_down_bird %= 2

    def get_sprite(self):
        return self.birds[self.up_or_down_bird]

    def check_position(self, bk_height, d_height):
        bird_height = self.get_sprite().image.get_size()[1] // 2
        if self.y > bk_height - bird_height + d_height:
            self.y = bk_height - bird_height + d_height
        elif self.y < bird_height + d_height:
            self.y = bird_height + d_height


class Background:
    def __init__(self, height):
        background = pygame.image.load(path.join(img_dir, 'background01.png')).convert()
        background = pygame.transform.rotozoom(
            background, 0, (height / background.get_height()) * ((height - 160) / height))
        self.sprites = [Sprite(background), Sprite(background)]
        self.dx = 0
        self.length = self.sprites[0].image.get_size()[0]
        self.height = background.get_height()

    def change_dx(self, time, bk_speed):
        self.dx = bk_speed * time
        if self.dx >= self.length:
            self.dx %= self.length

    def draw(self, canvas):
        self.length = self.sprites[0].image.get_size()[0]
        background_rect = [a / 2 for a in canvas.get_size()]
        x = self.sprites[0].image.get_size()[0]

        self.sprites[0].transform(center=background_rect)
        self.sprites[1].transform(center=background_rect)

        self.sprites[0].transform_relative(move=(- self.dx, 0))
        self.sprites[1].transform_relative(move=(x - self.dx, 0))

        self.sprites[0].draw(canvas)
        self.sprites[1].draw(canvas)

    def set_proper_size(self, height, canvas):
        for bk in self.sprites:
            bk = pygame.transform.rotozoom(canvas, 0, height / bk.image.get_size()[1])
        self.length = self.sprites[0].image.get_size()[0]


class VetaMiniGame(AbstractMiniGame):
    def configure(self, config_json):
        pass  # TODO

    def reset(self):
        pass  # TODO

    def __init__(self, life_time, set_speed=None):
        # set_speed should be scaling, not absolute parameter
        super().__init__(life_time)
        # TODO Если твоя игра расчитана на обределённый размер такта, необходимо бросить исключение
        # По умолчанию размер такта равен 4, но может произойти и иное
        # Это делается вот так:
        if self.beat_size != 4:
            raise AssertionError()  # Недействительный размер такта!
        self.time = 0
        self.width, self.height = 1080, 720
        self.d_height = 0
        self.bird = Bird()
        self.bk = None
        self.hole = None
        if not set_speed:
            self.speed = speed + rnd(- speed//5, speed//5)
        else:
            self.speed = set_speed * speed

    def update(self, time: dict):
        # kinda of gravitation for bird
        self.bird.y += self.height // 300 + self.bird.vy

        # changing birds wings every bit
        if time['beat_type'] in (1, 2):
            self.bird.change_bird()
            self.bird.vy = 0

        # calculating x for background and bird pictures
        d_time = self.time
        self.time = math.fabs(4 * time['bars'] + time['beats'] + time['delta'])
        d_time = self.time - d_time
        if self.bk:
            self.bk.change_dx(self.time, self.speed)

        # hole managing
        if self.hole and self.hole.should_be_destroyed:
            self.hole = Hole(rnd(self.height // 15, self.height // 7), self.bk.height, self.d_height,
                             rnd(0, 1))
            self.hole.dx = 0
        elif self.hole:
            self.hole.dx += self.speed * d_time

        delta_health = 0
        # checking whether inside a Gaussian distribution
        if self.hole:
            hole_under_bird_x = self.width - self.hole.dx + 3 * self.hole.sigma
            dx = int(math.fabs(int(hole_under_bird_x - self.width // 7)))
            if dx < 2 * self.hole.sigma:
                hole_y = self.hole.get_y(3 * self.hole.sigma - dx)
                if not self.hole.is_up:
                    if self.bird.y < hole_y:
                        delta_health = -5
                elif self.bird.y > self.bk.height - hole_y + 2 * self.d_height:
                    delta_health = -5

        return {'delta_health': delta_health, 'delta_score': 0}

    def draw(self, time: dict, canvas):
        self.width, self.height = canvas.get_size()
        if not self.bk:
            self.bk = Background(self.height)
            self.d_height = (self.height - self.bk.height) // 2
            self.hole = Hole(rnd(self.height // 15, self.height // 7), self.bk.height, self.d_height,
                             rnd(0, 1))

        self.bk.draw(canvas)

        self.bird.check_position(self.bk.height, self.d_height)
        self.bird.get_sprite().transform(center=(self.width // 7, self.bird.y))
        self.bird.get_sprite().draw(canvas)

        if self.hole and self.hole.dx > 2 * self.hole.points_delta and not self.hole.should_be_destroyed:
            pygame.draw.polygon(canvas, (0, 0, 0), self.hole.get_points(int(self.hole.dx), self.width))
            pygame.draw.aalines(canvas, (0, 0, 0), True,
                                self.hole.get_points(int(self.hole.dx), self.width))

    def handle(self, event):
        delta_score = 0
        if event['time']['beat_type'] in (1, 2):
            delta_score += 5 * event['time']['beat_type']

        if event['key']['key'] in (273, 119):
            self.bird.vy = - math.cos(math.pi * event['time']['delta']) * self.height // 50

        elif event['key']['key'] in (274, 115):
            self.bird.vy = + math.cos(math.pi * event['time']['delta']) * self.height // 50

        return {'delta_health': 0, 'delta_score': delta_score}
