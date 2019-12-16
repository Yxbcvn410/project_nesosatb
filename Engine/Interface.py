import abc


class AbstractUI(abc.ABC):
    @abc.abstractmethod
    def __init__(self, canvas):
        self.canvas = canvas
        self.runtime = None

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
        pass  # TODO

    def update_all(self):
        pass  # TODO

    def delete_animation(self, sprite):
        pass  # TODO

    def is_animating(self) -> bool:
        return not bool(self.animations)
