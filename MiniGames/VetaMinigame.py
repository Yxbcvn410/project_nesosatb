import pygame
import sys
from os import path
import math
from Engine.MiniGame import AbstractMiniGame
from Engine.Media import Sprite
from random import randint as rnd

img_dir = path.join(path.dirname(__file__), '../Assets/Artwork/img')


class HoleForVetaMiniGame:
    def __init__(self, sigma, height, is_up):
        self.sigma = sigma
        self.points_delta = 5
        self.points = []
        self.height = height
        self.should_be_destroyed = False
        self.make_points()
        self.is_up = is_up

    def make_points(self):
        number_of_points = (self.sigma * 6) // self.points_delta
        for i in range(number_of_points):
            y = math.exp(-(((i * self.points_delta - 3 * self.sigma) ** 2) / (2 * self.sigma ** 2)))
            self.points.append([i * self.points_delta, int(y * self.points_delta * self.sigma)])

    def get_y(self, x):
        return self.points[x // self.points_delta][1]

    def get_x(self, y):
        return int((2 * self.sigma ** 2 * math.log(y)) ** 0.5)

    def get_points(self, dx, width):
        moved_points = []

        if dx < self.sigma * 6:
            counter = dx // self.points_delta
        else:
            counter = (self.sigma * 6) // self.points_delta

        for i in range(counter):
            point = self.points[i]
            if self.is_up:
                moved_points.append([point[0] - dx + width, self.height - point[1]])
            else:
                moved_points.append([point[0] - dx + width, point[1]])

        if moved_points[-1][0] < self.points_delta:
            self.should_be_destroyed = True

        # making polygon up to the edge
        if self.is_up:
            moved_points.append([moved_points[-1][0], self.height])
            moved_points.append([width - dx, self.height])
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
        self.y = 100

    def change_bird(self):
        self.up_or_down_bird += 1
        self.up_or_down_bird %= 2

    def get_sprite(self):
        return self.birds[self.up_or_down_bird]


class Background:
    def __init__(self):
        background = pygame.image.load(path.join(img_dir, 'background01.png')).convert()
        background = pygame.transform.rotozoom(background, 0, 1.4)
        self.sprites = [Sprite(background), Sprite(background)]
        self.dx = 0
        self.length = self.sprites[0].image.get_size()[0]

    def change_dx(self, time):
        self.dx = 150 * time
        if self.dx >= self.length:
            self.dx %= self.length

    def draw(self, canvas, width, height):
        background_rect = [a / 2 for a in canvas.get_size()]
        self.sprites[0].transform(center=background_rect)
        self.sprites[1].transform(center=background_rect)

        self.sprites[0].transform_relative(move=(- self.dx, 0))
        x = self.sprites[0].image.get_size()[0]
        self.sprites[1].transform_relative(move=(x - self.dx, 0))

        self.sprites[0].draw(canvas)
        self.sprites[1].draw(canvas)


class VetaMiniGame(AbstractMiniGame):
    def __init__(self, life_time):
        super().__init__(life_time)
        self.width, self.height = 1080, 720
        self.bird = Bird()
        self.bk = Background()
        self.hole = HoleForVetaMiniGame(rnd(30, 80), 720, rnd(0, 1))
        self.hole_dx = 0

    def update(self, time: dict):
        # kinda of gravitation for bird
        self.bird.y += 1

        # changing birds wings every bit
        if time['beat_type'] in (1, 2):
            self.bird.change_bird()

        # calculating x for background and bird pictures
        time = math.fabs(4 * time['bars'] + time['beats'] + time['delta'])
        self.bk.change_dx(time)

        # hole managing
        if self.hole.should_be_destroyed:
            self.hole = HoleForVetaMiniGame(rnd(30, 80), self.height, rnd(0, 1))
            self.hole_dx = 0
        else:
            self.hole_dx += 10

        delta_health = 0
        delta_score = 1
        # checking whether inside a Gaussian distribution
        if self.hole:
            hole_under_bird_x = self.width - self.hole_dx + 3 * self.hole.sigma
            dx = int(math.fabs(int(hole_under_bird_x - 200)))
            if dx < 2 * self.hole.sigma:
                hole_y = self.hole.get_y(3 * self.hole.sigma - dx)
                if self.hole.is_up:
                    if self.bird.y > hole_y:
                        delta_health = -5
                        delta_score = 0
                elif self.bird.y < self.height - hole_y:
                    delta_health = -5
                    delta_score = 0

        return {'delta_health': delta_health, 'delta_score': delta_score}

    def draw(self, time: dict, canvas):
        self.width, self.height = canvas.get_size()

        self.bk.draw(canvas, self.width, self.height)

        bird_height = self.bird.get_sprite().image.get_size()[1] // 2
        if self.bird.y > self.height - bird_height:
            self.bird.y = self.height - bird_height
        elif self.bird.y < bird_height:
            self.bird.y = bird_height

        self.bird.get_sprite().transform(center=(200, self.bird.y))
        self.bird.get_sprite().draw(canvas)

        if self.hole and self.hole_dx > 2 * self.hole.points_delta and not self.hole.should_be_destroyed:
            pygame.draw.polygon(canvas, (0, 0, 0), self.hole.get_points(int(self.hole_dx), self.width))
            pygame.draw.aalines(canvas, (0, 0, 0), True,
                                self.hole.get_points(int(self.hole_dx), self.width))

    def handle(self, event):
        if event['time']['beat_type'] > 0:
            if event['key']['key'] in (273, 119):
                self.bird.y += 10 * math.log(math.fabs(event['time']['delta']), 50)
            elif event['key']['key'] in (274, 115):
                self.bird.y -= 10 * math.log(math.fabs(event['time']['delta']), 50)

        return {'delta_health': 0, 'delta_score': 0}
