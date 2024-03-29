import pygame


class Sprite:
    def __init__(self, image):
        if type(image) == str:
            self.image = pygame.image.load(image)
        elif type(image) == pygame.Surface:
            self.image = image
        else:
            raise TypeError  # Тип изображения не поддерживается!

        self.center = [0, 0]
        self.turn = 0
        self.scale = 1
        self.opacity = 1
        self.temp = None

    def transform(self, **kwargs):
        if 'center' in kwargs:
            self.center = list(kwargs['center'])
            if 'x' in kwargs or 'y' in kwargs:
                raise AssertionError  # Конфликт ключевых слов!
        if 'angle' in kwargs:
            self.turn = kwargs['angle']
        if 'scale' in kwargs:
            self.scale = kwargs['scale']
        if 'x' in kwargs:
            self.center[0] = kwargs['x']
        if 'y' in kwargs:
            self.center[1] = kwargs['y']
        if 'opacity' in kwargs:
            self.opacity = kwargs['opacity']

    def transform_relative(self, **kwargs):
        if 'move' in kwargs:
            self.center = [sum(pt) for pt in zip(self.center, kwargs['move'])]
        if 'turn' in kwargs:
            self.turn += kwargs['turn']
        if 'scale' in kwargs:
            self.scale *= kwargs['scale']
        if 'move_x' in kwargs:
            self.center[0] += kwargs['move_x']
        if 'move_y' in kwargs:
            self.center[1] += kwargs['move_y']

    def get_property(self, number_only=False):
        return {
            'center': self.center,
            'angle': self.turn,
            'scale': self.scale,
            'opacity': self.opacity
        } if not number_only else {
            'x': self.center[0],
            'y': self.center[1],
            'angle': self.turn,
            'scale': self.scale,
            'opacity': self.opacity
        }

    def __blit_alpha__(self, target, source, location, opacity):
        self.temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        self.temp.blit(target, tuple(-x for x in location))
        self.temp.blit(source, (0, 0))
        self.temp.set_alpha(opacity * 255)
        target.blit(self.temp, location)

    def draw(self, surface):
        transformed_instance = self.image
        if self.turn != 0 or self.scale != 1:  # Если не нужно менять размер - не надо
            transformed_instance = pygame.transform.rotozoom(transformed_instance, self.turn, self.scale)
        left_upper_angle = tuple(pt[0] - pt[1] * 0.5 for pt in zip(self.center, transformed_instance.get_size()))
        if self.opacity != 1:  # Если нет прозрачности, можно использовать прямую отрисовку
            self.__blit_alpha__(surface, transformed_instance, left_upper_angle, self.opacity)
        else:
            surface.blit(transformed_instance, left_upper_angle)

    def fill(self, surface):
        center = [a / 2 for a in surface.get_size()]
        required_k = max(a[1] / a[0] for a in zip(self.image.get_size(), surface.get_size()))
        prop = self.get_property()
        self.transform(center=center, angle=0, scale=required_k, opacity=1)
        self.draw(surface)
        self.transform(**prop)


class AnimationSprite(Sprite):
    def __init__(self, images: dict):
        if len(images) == 0:
            raise AssertionError()  # Пустой список спрайтов
        super().__init__(list(images.values())[0])
        self.all_images = images
        for image_key in self.all_images:
            if type(self.all_images[image_key]) == str:
                self.all_images[image_key] = pygame.image.load(self.all_images[image_key])
            if not type(self.all_images[image_key]) == pygame.Surface:
                raise TypeError()  # Тип изображения не поддерживается!

    def set_active_sprite(self, key):
        self.image = self.all_images[key]
