import abc


class AbstractMiniGame(abc.ABC):
    @abc.abstractmethod
    def __init__(self, start_time_bars, life_time_bars):
        self.start_time = start_time_bars
        self.life_time = life_time_bars
        self.event_queue = []
        self.score = 0

    def is_over(self, time: dict):
        return time['bars'] >= self.start_time + self.life_time

    @abc.abstractmethod
    def update(self, time: dict) -> dict:
        pass

    @abc.abstractmethod
    def handle(self, event):
        pass

    @abc.abstractmethod
    def draw(self, time: dict,  graphical_ui):
        pass
