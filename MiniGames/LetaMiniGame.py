import pygame
from os import path
import math
from Engine.MiniGame import AbstractMiniGame
from Engine.Media import Sprite
from random import choice

img_dir = path.join(path.dirname(__file__), '../Assets/Artwork/img')
bar_width = 80
beats_number = 4


class LetaMiniGame(AbstractMiniGame):
    def __init__(self, life_time, letters=None):
        super().__init__(life_time)
        self.letters = letters
        if letters is None:
            self.create_letters(life_time)
        self.len_letters = len(self.letters)

        # whether recieved data is correct for game logic and fixing it
        if len(self.letters) > (life_time - 1) // 2:
            self.letters = self.letters[:(life_time - 1) // 2]
            self.len_letters = len(self.letters)
        for i in range(self.len_letters):
            if len(self.letters[i]) > beats_number:
                self.letters[i] = self.letters[i][:beats_number]
            elif len(self.letters[i]) < beats_number:
                for j in range(beats_number - len(self.letters[i])):
                    self.letters[i].append(choice(['w', 's', 'a', 'd']))

        self.counter = 0
        self.background = Sprite(pygame.image.load(path.join(img_dir, 'orange.jpg')).convert())
        self.height, self.width = 0, 0
        self.got_or_not = [[0] * beats_number for i in range(self.len_letters)]
        self.font_size = 0

    def update(self, time: dict):
        if time['bars'] > self.counter:
            self.counter += 1

        delta_health = 0
        delta_score = 0
        if time['beat_type'] in (1, 2) and self.len_letters < self.counter and \
                self.got_or_not[(time['bars'] - 1) % self.len_letters][time['beats']] == 0:
            self.got_or_not[(time['bars'] - 1) % self.len_letters][time['beats']] = -1
            delta_health = -5

        return {'delta_health': delta_health, 'delta_score': delta_score}

    def draw(self, time: dict, canvas):
        # getting proper sizes and background
        self.width, self.height = canvas.get_size()
        background_rect = [a / 2 for a in canvas.get_size()]
        self.background.transform(center=background_rect,
                                  scale=(self.height - 2 * bar_width) / self.background.image.get_size()[1])
        self.background.draw(canvas)
        self.font_size = int((self.height - 2 * bar_width) / (2 * self.len_letters))

        # displaying letters
        if self.counter <= self.len_letters:
            self.write_letters(canvas, self.counter)
        else:
            # when it s time for printing
            self.write_letters(canvas, self.len_letters)

            # checking some or all lines
            if self.counter < 2 * self.len_letters:
                number_of_lines = (self.counter - 1) % self.len_letters + 1
            else:
                number_of_lines = self.len_letters

            # marking letters
            for i in range(number_of_lines):
                for j in range(beats_number):
                    # circle for pressed ones
                    if self.got_or_not[i][j] == 1:
                        pygame.draw.circle(
                            canvas, (250, 250, 250),
                            [self.width // 2 + int((j - (len(self.letters[i]) - 1) / 2) * self.font_size),
                             int(1.05 * bar_width) + int((i + 1) * (self.height - 2 * bar_width) / (self.len_letters +
                                                                                                    1))],
                            int(self.font_size // 2.5), int(self.font_size // 20))

                    # crosses for missed ones
                    elif self.got_or_not[i][j] == -1:
                        # center x and y for a letter
                        x = self.width // 2 + int((j - (len(self.letters[i]) - 1) / 2) * self.font_size)
                        y = bar_width + int((i + 1) * (self.height - 2 * bar_width) / (self.len_letters + 1))

                        pygame.draw.line(canvas, (250, 250, 250),
                                         [x + self.font_size // 3, y + self.font_size // 3],
                                         [x - self.font_size // 3, y - self.font_size // 3],
                                         5)
                        pygame.draw.line(canvas, (250, 250, 250),
                                         [x - self.font_size // 3, y + self.font_size // 3],
                                         [x + self.font_size // 3, y - self.font_size // 3],
                                         5)

    def handle(self, event):
        delta_score = 0
        delta_health = 0
        if self.counter > self.len_letters and event['key']['unicode'] in ('w', 's', 'a', 'd') \
                and math.fabs(event['time']['delta']) < 0.2:
            bars = (event['time']['bars'] - 1) % self.len_letters
            beats = event['time']['beats']

            # new press on already pressed correctly letter also counts
            if event['key']['unicode'] == self.letters[bars][beats]:
                if self.got_or_not[bars][beats] == -1:
                    # if the letter was already marked wrong we return health back
                    delta_health += 5

                self.got_or_not[bars][beats] = 1
                delta_score += 5

            # if the event_key was already accepted we dont charge for new wrong
            elif self.letters[bars][beats] != 1:
                delta_health -= 5
                self.got_or_not[bars][beats] = -1

        return {'delta_health': delta_health, 'delta_score': delta_score}

    def write_letters(self, canvas, counter):

        font = pygame.font.Font('Assets/Fonts/Patapon.ttf', self.font_size)

        for i in range(counter):
            for j in range(len(self.letters[i])):
                pause_text = font.render(self.letters[i][j], 1, (250, 250, 250))
                canvas.blit(pause_text, pause_text.get_rect(
                    center=[self.width // 2 + (j - (len(self.letters[i]) - 1) / 2) * self.font_size,
                            bar_width + (i + 1) * (self.height - 2 * bar_width) / (self.len_letters + 1)]))

    def create_letters(self, life_time):
        self.letters = []
        for i in range((life_time - 1) // 2):
            line = []
            for j in range(beats_number):
                line.append(choice(['w', 's', 'd', 'a']))
            self.letters.append(line)
