import pygame


class MusicPlayer:
    def __init__(self):
        self.music = None  # TODO

    def load(self, file):
        print('Loaded music from {}'.format(file))  # TODO

    def play(self):
        print('Playback started')  # TODO

    def pause(self):
        print('Playback paused')  # TODO


class Sprite:
    def __init__(self, image):
        if type(image) == str:
            self.image = pygame.image.load(image)
        elif type(image) == pygame.Surface:
            self.image = image
        else:
            raise TypeError  # Image type not supported

        self.center = (0, 0)
        self.turn = 0
        self.scale = 1
        self.opacity = 1
        self.temp = None

    def transform(self, **kwargs):
        if 'center' in kwargs:
            self.center = kwargs['center']
        if 'angle' in kwargs:
            self.turn = kwargs['angle']
        if 'scale' in kwargs:
            self.scale = kwargs['scale']

    def transform_relative(self, **kwargs):
        if 'move' in kwargs:
            self.center = (sum(pt) for pt in zip(self.center, kwargs['move']))
        if 'turn' in kwargs:
            self.turn += kwargs['turn']
        if 'scale' in kwargs:
            self.scale *= kwargs['scale']

    def set_opacity(self, opacity):
        self.opacity = opacity

    def __blit_alpha__(self, target, source, location, opacity):
        self.temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        self.temp.blit(target, tuple(-x for x in location))
        self.temp.blit(source, (0, 0))
        self.temp.set_alpha(opacity * 255)
        target.blit(self.temp, location)

    def draw(self, surface):
        transformed_instance = pygame.transform.rotozoom(self.image, self.turn, self.scale)
        left_upper_angle = tuple(pt[0] - pt[1] * 0.5 for pt in zip(self.center, transformed_instance.get_size()))
        self.__blit_alpha__(surface, transformed_instance, left_upper_angle, self.opacity)
