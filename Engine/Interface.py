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
    def draw_widgets(self):
        """Рисует на экране виджеты. Вызывается синхронно с FPS"""
        pass

    def clean_canvas(self):
        """Очищает холст"""
        self.canvas.fill((0, 0, 0))
