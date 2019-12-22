import pygame

from Engine.Media import Sprite
from Engine.MiniGame import AbstractMiniGame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (188, 188, 0)

X_STEP = 200
Y_STEP = 200
RADIUS = 180

LETTER_COLOURS = {'w': BLUE, 'a': GREEN, 's': YELLOW, 'd': RED, 'ц': BLUE, 'ф': GREEN, 'ы': YELLOW, 'в': RED, '': BLACK}


class Letter(Sprite):
    def render_letter(self, letter):
        font = pygame.font.Font('Assets/Fonts/Patapon.ttf', 4 * RADIUS // 5)
        letter_surf = font.render(letter, 1, BLACK)
        image = pygame.Surface((RADIUS, RADIUS), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.ellipse(image, LETTER_COLOURS[letter],
                            [0, 0, RADIUS, RADIUS])
        pygame.draw.ellipse(image, WHITE, [0, 0, RADIUS, RADIUS], 10)
        image.blit(letter_surf, letter_surf.get_rect(center=(RADIUS // 2, RADIUS // 2)))
        self.image = image

    def __init__(self, letter: str):
        self.render_letter(letter)
        self.letter = letter
        super().__init__(self.image)

    def set_state(self, ok):
        self.render_letter(self.letter)
        if ok:
            pygame.draw.ellipse(self.image, (0, 155, 0), [0, 0, RADIUS, RADIUS], 20)
        else:
            pygame.draw.line(self.image, (155, 0, 0), (0, 0), (RADIUS, RADIUS), 20)
            pygame.draw.line(self.image, (155, 0, 0), (0, RADIUS), (RADIUS, 0), 20)


class LetterMiniGame(AbstractMiniGame):
    def load_letters(self, letters):
        for i in range(len(letters)):
            letters[i].extend([''] * self.beat_size)
        letters.extend([[''] * self.beat_size] * ((self.life_time - self.cool_down) // 2))
        self.letters = [line[:self.beat_size] for line in letters[:(self.life_time - self.cool_down) // 2]]
        self.letter_sprites = [[Letter(letter) for letter in line] for line in self.letters]

    def __init__(self, life_time_bars, letters=None, beat_size=4):
        super().__init__(life_time_bars, beat_size)
        if letters is None:
            letters = [['w', 'a', 's', 'd']]
        self.cool_down = 0
        self.bg = Sprite('Assets/Artwork/img/LetaMiniGame/orange.jpg')
        self.letters = []
        self.letter_sprites = []
        self.load_letters(letters)
        self.current_pressed_letter = None

    def update(self, time: dict) -> dict:
        delta_health = 0
        if ((self.life_time - self.cool_down) // 2) * 2 > time['bars'] >= (self.life_time - self.cool_down) // 2:
            x = time['beats']
            y = time['bars'] - (self.life_time - self.cool_down) // 2
            if time['beat_type'] in (1, 2):
                if self.current_pressed_letter is None:
                    self.letter_sprites[y][x].set_state(self.letter_sprites[y][x].letter == '')
            if time['beat_type'] == -1:
                if self.current_pressed_letter is None and self.letter_sprites[y][x].letter != '':
                    delta_health = -5
                self.current_pressed_letter = None
        return {'delta_health': delta_health, 'delta_score': 0}

    def handle(self, event):
        delta_health = 0
        delta_score = 0
        if event['key']['unicode'] in LETTER_COLOURS and \
                ((self.life_time - self.cool_down) // 2) * 2 > event['time']['bars'] >= (
                self.life_time - self.cool_down) // 2:
            x = event['time']['beats']
            y = event['time']['bars'] - (self.life_time - self.cool_down) // 2
            if self.current_pressed_letter is None:
                self.current_pressed_letter = event['key']['unicode']
            if self.current_pressed_letter == self.letter_sprites[y][x].letter:
                delta_score = 10
                self.letter_sprites[y][x].set_state(True)
            else:
                delta_health = -5
                self.letter_sprites[y][x].set_state(False)

        return {'delta_health': delta_health, 'delta_score': delta_score}

    def draw(self, time: dict, canvas):
        size = canvas.get_size()
        self.bg.transform(center=[a / 2 for a in size])
        self.bg.fill(canvas)
        vis_size = ((self.beat_size - 1) * X_STEP, (len(self.letters) - 1) * Y_STEP)
        move = tuple((size[i] - vis_size[i]) / 2 for i in range(2))
        if time['bars'] < (self.life_time - self.cool_down) // 2:
            for spr_line in self.letter_sprites:
                for letter_spr in spr_line:
                    y = self.letter_sprites.index(spr_line)
                    x = spr_line.index(letter_spr)
                    if time['bars'] > y or (
                            time['bars'] == y and (time['beats'] > x or (time['beats'] == x and time['delta'] > 0))):
                        letter_spr.transform(center=(x * X_STEP, y * Y_STEP))
                        letter_spr.transform_relative(move=move)
                        letter_spr.draw(canvas)
        elif time['bars'] < ((self.life_time - self.cool_down) // 2) * 2:
            for spr_line in self.letter_sprites:
                for letter_spr in spr_line:
                    y = self.letter_sprites.index(spr_line)
                    x = spr_line.index(letter_spr)
                    letter_spr.transform(center=(x * X_STEP, y * Y_STEP))
                    letter_spr.transform_relative(move=move)
                    letter_spr.draw(canvas)

    def configure(self, config_json):
        if 'cooldown' in config_json:
            self.cool_down = config_json['cooldown']
        if 'letters' in config_json:
            self.load_letters(config_json['letters'])
        if 'bg' in config_json:
            self.bg = Sprite(config_json['bg'])

    def reset(self):
        pass
