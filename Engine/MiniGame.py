import abc


class AbstractMiniGame(abc.ABC):
    @abc.abstractmethod
    def __init__(self, life_time_bars):
        self.start_time = 0
        self.life_time = life_time_bars
        self.event_queue = []

    def is_over(self, time: dict):
        """Встроенный метод, не переопределяем"""
        return time['bars'] >= self.start_time + self.life_time

    @abc.abstractmethod
    def update(self, time: dict) -> dict:
        """Обновить данные мини-игры в соответствии со временем
        Возвращает статус игры - закончилась ли игра и количество очков"""
        return {'delta_health': 0, 'delta_score': 0}

    @abc.abstractmethod
    def handle(self, event):
        """Обработать событие нажатия клавиши
        Возврат изменения статуса игры"""
        return {'delta_health': 0, 'delta_score': 0}

    @abc.abstractmethod
    def draw(self, time: dict, graphical_ui):
        """Отрисовать компоненты мини-игры"""
        pass


class MiniGameWrapper(AbstractMiniGame):
    def __init__(self):
        super().__init__(0)
        self.__mini_games = []
        self.active_mini_game = None

    def append_mini_game(self, mini_game, offset=0):
        """Добавляем мини-игру. По-другому добавлять мини-игры нельзя!"""
        if mini_game.start_time != 0:
            raise AssertionError()  # Мини-игра уже сдвинута!
        self.__mini_games.append(mini_game)
        self.__mini_games[-1].start_time += offset + self.life_time
        self.active_mini_game = self.__get_nearest_future_mini_game({'bars': 0})
        self.life_time = max(self.life_time, mini_game.start_time + mini_game.life_time)

    def __get_nearest_future_mini_game(self, time: dict):
        """Ищем ближайшую мини-игру в будущем"""
        nearest_mini_game = None
        for mini_game in self.__mini_games:
            if (mini_game.start_time >= time['bars']) and (
                    (nearest_mini_game is None) or (nearest_mini_game.start_time > mini_game.start_time)):
                nearest_mini_game = mini_game
        return nearest_mini_game

    def update(self, time: dict):
        """Обновить текущую мини-игру"""
        if self.active_mini_game.is_over(time):
            # Текущая мини-игра закончилась, ищем следующую
            self.active_mini_game = self.__get_nearest_future_mini_game(time)

        if self.active_mini_game:
            # Если есть мини-игра в будущем, обновляем и рисуем
            minigame_time = dict(time)
            minigame_time['bars'] -= self.active_mini_game.start_time
            return self.active_mini_game.update(minigame_time)
        # Уровень закончился, мини-игр больше нет
        return {'delta_health': 0, 'delta_score': 0}

    def handle(self, event):
        """Передать мини-игре событие нажатия"""
        if self.active_mini_game:
            event['time']['bars'] -= self.active_mini_game.start_time
            return self.active_mini_game.handle(event)
        return {'delta_health': 0, 'delta_score': 0}
        # То, как событие отобразится на графическом представлении, определяет мини-игра

    def draw(self, time: dict, graphical_ui):
        if self.active_mini_game:
            if self.active_mini_game.start_time > time['bars']:
                graphical_ui.clean_canvas()
            else:
                self.active_mini_game.draw(time, graphical_ui)