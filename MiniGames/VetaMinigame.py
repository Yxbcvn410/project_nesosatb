import pygame
import sys
from os import path
import math
from Engine.MiniGame import AbstractMiniGame
from Engine.Media import Sprite
from random import randint as rnd


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

        if self.is_up:
            moved_points.append([moved_points[-1][0], self.height])
            moved_points.append([width - dx, self.height])
        else:
            moved_points.append([moved_points[-1][0], 0])
            moved_points.append([width - dx, 0])

        return moved_points


class VetaMiniGame(AbstractMiniGame):
    def __init__(self, life_time):
        super().__init__(life_time)
        self.width, self.height = 1080, 720
        img_dir = path.join(path.dirname(__file__), '../Assets/Artwork/img')
        background = pygame.image.load(path.join(img_dir, 'background01.png')).convert()
        background = pygame.transform.rotozoom(background, 0, 1.4)
        self.backgrounds = [Sprite(background), Sprite(background)]
        self.dx = 0
        self.bk_length = self.backgrounds[0].image.get_size()[0]
        bird_up = pygame.image.load(path.join(img_dir, 'rose_up.png')).convert_alpha()
        bird_up = pygame.transform.rotozoom(bird_up, 0, 0.2)
        bird_down = pygame.image.load(path.join(img_dir, 'rose_down.png')).convert_alpha()
        bird_down = pygame.transform.rotozoom(bird_down, 0, 0.2)
        self.bird = [Sprite(bird_up), Sprite(bird_down)]
        self.up_or_down_bird = 0
        self.bird_y = 100
        self.time = 0
        self.hole = HoleForVetaMiniGame(rnd(30, 80), 720, rnd(0, 1))
        self.hole_dx = 0

    def update(self, time: dict):
        # kinda of gravitation for bird
        self.bird_y += 1

        # changing birds wings every bit
        if time['beat_type'] in (1, 2):
            self.up_or_down_bird += 1
            self.up_or_down_bird %= 2

        # calculating x for background and bird pictures
        self.time = math.fabs(4 * time['bars'] + time['beats'] + time['delta'])
        self.dx = 150 * self.time
        if self.dx >= self.bk_length:
            self.dx %= self.bk_length

        # hole managing
        if self.hole.should_be_destroyed:
            self.hole = HoleForVetaMiniGame(rnd(30, 80), self.height, rnd(0, 1))
            self.hole_dx = 0
        else:
            self.hole_dx += 10

        delta_health = 0
        # checking whether inside a Gaussian distribution
        if self.hole:
            hole_under_bird_x = self.width - self.hole_dx + 3 * self.hole.sigma
            dx = int(math.fabs(int(hole_under_bird_x - 200)))
            if dx < 2 * self.hole.sigma:
                hole_y = self.hole.get_y(3 * self.hole.sigma - dx)
                if self.hole.is_up:
                    if self.bird_y > hole_y:
                        delta_health = -5
                elif self.bird_y < self.height - hole_y:
                    delta_health = -5

        return {'delta_health': delta_health, 'delta_score': 0}

    def draw(self, time: dict, graphical_ui):
        self.width, self.height = graphical_ui.canvas.get_size()
        background_rect = [a / 2 for a in graphical_ui.canvas.get_size()]
        self.backgrounds[0].transform(center=background_rect)
        self.backgrounds[1].transform(center=background_rect)
        bird_height = self.bird[self.up_or_down_bird].image.get_size()[1] // 2

        if self.bird_y > self.height - bird_height:
            self.bird_y = self.height - bird_height
        elif self.bird_y < bird_height:
            self.bird_y = bird_height

        self.bird[self.up_or_down_bird].transform(center=(200, self.bird_y))
        self.backgrounds[0].transform_relative(move=(- self.dx, 0))
        x = self.backgrounds[0].image.get_size()[0]
        self.backgrounds[1].transform_relative(move=(x - self.dx, 0))

        self.backgrounds[0].draw(graphical_ui.canvas)
        self.backgrounds[1].draw(graphical_ui.canvas)
        self.bird[self.up_or_down_bird].draw(graphical_ui.canvas)
        if self.hole and self.hole_dx > 2 * self.hole.points_delta and not self.hole.should_be_destroyed:
            pygame.draw.polygon(graphical_ui.canvas, (0, 0, 0), self.hole.get_points(int(self.hole_dx), self.width))
            pygame.draw.aalines(graphical_ui.canvas, (0, 0, 0), True, self.hole.get_points(int(self.hole_dx), self.width))

    def handle(self, event):
        # sys.stdout.write(str(event) + '\n')
        # sys.stdout.flush()
        if event['time']['beat_type'] > 0:
            if event['key']['key'] in (273, 119):
                self.bird_y += 10 * math.log10(math.fabs(event['time']['delta']))
            elif event['key']['key'] in (274, 115):
                self.bird_y -= 10 * math.log10(math.fabs(event['time']['delta']))

        return {'delta_health': 0, 'delta_score': 0}
