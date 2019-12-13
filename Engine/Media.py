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
        self.image = self.image.convert()

        self.center = (0, 0)
        self.turn = 0
        self.scale = 1
        self.opacity = 1

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

    def draw(self, surface):
        transformed_instance = pygame.transform.rotozoom(self.image, self.turn, self.scale)
        transformed_instance.set_alpha(int(self.opacity * 255))
        left_upper_angle = tuple(pt[0] - pt[1] * 0.5 for pt in zip(self.center, transformed_instance.get_size()))
        surface.blit(transformed_instance, left_upper_angle)
