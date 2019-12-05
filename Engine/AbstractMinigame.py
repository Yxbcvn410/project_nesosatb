import abc


class AbstractMiniGame(abc.ABC):
    @abc.abstractmethod
    def __init__(self, start_time_bars, life_time_bars, canvas):
        self.start_time = start_time_bars
        self.life_time = life_time_bars
        self.event_queue = []
        self.score = 0
        self.health_lost = 0
        self.canvas = canvas

    def is_over(self, time: dict):
        """Встроенный метод, не переопределяем"""
        return time['bars'] >= self.start_time + self.life_time

    @abc.abstractmethod
    def update(self, time: dict) -> dict:
        """Обновить данные мини-игры в соответствии со временем"""
        pass

    @abc.abstractmethod
    def handle(self, event):
        """Обработать событие нажатия клавиши"""
        pass

    @abc.abstractmethod
    def draw(self, time: dict, graphical_ui):
        """Отрисовать компоненты мини-игры"""
        pass
