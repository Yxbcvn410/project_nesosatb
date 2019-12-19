import abc
from Engine.Level import FPS


class AbstractUI(abc.ABC):
    @abc.abstractmethod
    def __init__(self, canvas):
        self.canvas = canvas
        self.runtime = None

    @abc.abstractmethod
    def load_views(self, views: dict):
        """Загружаем возможные интерфейсы для перехода. Каждый элемент - пара (UI, runtime)"""
        pass

    def set_runtime(self, runtime):
        """Runtime - объект, контроллирующий выполнение. Можно в него вынести обработку нажатия."""
        self.runtime = runtime

    @abc.abstractmethod
    def key_press(self, key):
        """Обработать нажатие клавиши. Возвращать новое представление (Экземпляр AbstractUI) если его нужно изменить."""
        pass

    @abc.abstractmethod
    def update(self):
        """Обновляется, обновляет рантайм если есть. Вызывается синхронно с FPS."""
        pass

    @abc.abstractmethod
    def draw_widgets(self):
        """Рисует на экране виджеты."""
        pass

    def clean_canvas(self):
        """Очищает холст"""
        self.canvas.fill((0, 0, 0))


class AnimationRuntime:
    def __init__(self):
        self.animations = []

    def add_animation(self, sprite, time, final_state: dict):
        self.animations.append([sprite, time, final_state])

    def update_all(self, surface):
        dt = 1 / FPS
        i = 0
        while i < len(self.animations):
            with self.animations[i] as animation:
                sprite = animation[0]
                kwargs = sprite.get_property()
                for key in kwargs:
                    kwargs[key] = dt * (animation[2][key] - kwargs[key]) / animation[1]
                sprite.transform_relative(**kwargs)
                sprite.draw(surface)
                animation[1] -= dt
                if animation[1] < 0:
                    sprite.transform(**(animation[2]))
                    self.animations.pop(i)
                    i -= 1
                i += 1

    def delete_animation(self, sprite):
        sprites = [animation[0] for animation in self.animations]
        if sprite in sprites:
            return self.animations.pop(sprites.index(sprite))[2]

    def is_animating(self) -> bool:
        return not bool(self.animations)
