import math
from os import path
from random import choice

import pygame

from Engine.Media import Sprite
from Engine.MiniGame import AbstractMiniGame

# This game is about pressing one of [w, s, a, d] Every tact has a line of letters
# for every beat each. Dor the first half of the game we only display for every moment only
# those letters that relate to this musical moment or earlier one
# and then with all letters displayed we check if player prints them

img_dir = path.join(path.dirname(__file__), '../Assets/Artwork/img/LetaMiniGame/')
bar_width = 80
beats_number = 4
characters = ('w', 's', 'a', 'd')


class LetaMiniGame(AbstractMiniGame):
    def reset(self):
        pass

    def configure(self, config_json):
        self.letters = config_json['letters']

        if self.letters is None:
            self.letters = self.create_letters(self.life_time)
        self.len_letters = len(self.letters)

        # whether received data is correct for game logic and fixing it

        # how many lines
        if self.len_letters > (self.life_time - 1) // 2:
            self.letters = self.letters[:(self.life_time - 1) // 2]
            self.len_letters = len(self.letters)
        elif self.len_letters < (self.life_time - 1) // 2:
            additional_lines = self.create_letters((self.life_time - 1) // 2 - self.len_letters)
            for line in additional_lines:
                self.letters.append(line)
            self.len_letters = len(self.letters)

        # how many letters in every line
        for i in range(self.len_letters):
            if len(self.letters[i]) > beats_number:
                self.letters[i] = self.letters[i][:beats_number]
            elif len(self.letters[i]) < beats_number:
                for j in range(beats_number - len(self.letters[i])):
                    self.letters[i].append(choice(characters))

        self.got_or_not = [[0] * beats_number for i in range(self.len_letters)]
        self.background = Sprite(pygame.image.load(path.join(img_dir, config_json['background'])).convert())

    def __init__(self, life_time):
        super().__init__(life_time)
        self.letters = None
        self.len_letters = 0
        self.counter = 0
        self.letter_counter = 0
        self.background = None
        self.height, self.width = 0, 0
        self.got_or_not = []
        self.font_size = 0

    def update(self, time: dict):
        if time['bars'] > self.counter and time['beat_type'] in (1, 2):
            self.counter += 1
        if (time['beats'] > self.letter_counter or time['beats'] == 0) and time['beat_type'] in (1, 2):
            self.letter_counter = time['beats']

        delta_health = 0
        delta_score = 0

        if time['beat_type'] in (1, 2) and self.len_letters < self.counter and \
                self.got_or_not[(self.counter - 1) % self.len_letters][self.letter_counter] == 0:
            self.got_or_not[(self.counter - 1) % self.len_letters][self.letter_counter] = -1
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
        if self.counter > self.len_letters and event['key']['unicode'] in characters \
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
            # last line only already beated letters if it's first half
            if i == counter - 1 and self.counter <= self.len_letters:
                local_counter = self.letter_counter + 1
            else:
                local_counter = beats_number

            for j in range(local_counter):
                pause_text = font.render(self.letters[i][j], 1, (250, 250, 250))
                canvas.blit(pause_text, pause_text.get_rect(
                    center=[self.width // 2 + (j - (len(self.letters[i]) - 1) / 2) * self.font_size,
                            bar_width + (i + 1) * (self.height - 2 * bar_width) / (self.len_letters + 1)]))

    def create_letters(self, line_number):
        letters = []
        for i in range(line_number):
            line = []
            for j in range(beats_number):
                line.append(choice(characters))
            letters.append(line)
        return letters
