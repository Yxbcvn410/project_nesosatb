import abc


class AbstractMiniGame(abc.ABC):
    @abc.abstractmethod
    def __init__(self, life_time_bars, beat_size=4):
        self.start_time = 0
        self.life_time = life_time_bars
        self.event_queue = []
        self.beat_size = beat_size

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
    def draw(self, time: dict, canvas):
        """Отрисовать компоненты мини-игры"""
        pass

    @abc.abstractmethod
    def reset(self):
        """Сбросить данные уровня, чтобы начать игру сначала"""
        pass


class MiniGameWrapper(AbstractMiniGame):
    def __init__(self):
        super().__init__(0)
        self.__mini_games = []
        self.active_mini_game = None
        self.current_mini_game_score = 0
        self.beat_size = 0

    def append_mini_game(self, mini_game, offset=0):
        """Добавляем мини-игру. По-другому добавлять мини-игры нельзя!"""
        if mini_game.start_time != 0:
            raise AssertionError()  # Мини-игра уже сдвинута!
        if offset < 0:
            raise ValueError()  # Наложение мини-игр по времени недопустимо!
        if self.beat_size == 0:
            self.beat_size = mini_game.beat_size
        if self.beat_size != mini_game.beat_size:
            raise AssertionError()  # Размеры содержимых мини-игр не совпадают!
        self.__mini_games.append(mini_game)
        self.__mini_games[-1].start_time = offset + self.life_time
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
        current_mini_game_stats = {'delta_health': 0, 'delta_score': 0}
        if self.active_mini_game is None:
            # Уровень закончился, мини-игр больше нет
            return current_mini_game_stats

        if self.active_mini_game.is_over(time):
            # Текущая мини-игра закончилась, ищем следующую
            self.current_mini_game_score = 0
            self.active_mini_game = self.__get_nearest_future_mini_game(time)
            if self.active_mini_game is None:
                return current_mini_game_stats

        # Если есть мини-игра в будущем, обновляем
        minigame_time = dict(time)
        minigame_time['bars'] -= self.active_mini_game.start_time
        if minigame_time['bars'] >= 0:
            current_mini_game_stats = self.active_mini_game.update(minigame_time)
        self.current_mini_game_score += current_mini_game_stats['delta_score']
        return current_mini_game_stats

    def handle(self, event):
        """Передать мини-игре событие нажатия"""
        current_mini_game_stats = {'delta_health': 0, 'delta_score': 0}
        if self.active_mini_game:
            event['time']['bars'] -= self.active_mini_game.start_time
            if event['time']['bars'] >= 0:
                current_mini_game_stats = self.active_mini_game.handle(event)
        self.current_mini_game_score += current_mini_game_stats['delta_score']
        return current_mini_game_stats
        # То, как событие отобразится на графическом представлении, определяет мини-игра

    def draw(self, time: dict, canvas):
        if self.active_mini_game:
            minigame_time = dict(time)
            minigame_time['bars'] -= self.active_mini_game.start_time
            if minigame_time['bars'] >= 0:
                self.active_mini_game.draw(minigame_time, canvas)

    def reset(self):
        self.active_mini_game = self.__get_nearest_future_mini_game({'bars': 0})
        self.current_mini_game_score = 0
        self.event_queue = []
        for minigame in self.__mini_games:
            minigame.reset()

    def get_waypoints(self):
        last_mini_game_type = None
        waypoints = []
        for mini_game in self.__mini_games:
            if type(mini_game) != last_mini_game_type:
                waypoints.append(mini_game.start_time)
                last_mini_game_type = type(mini_game)
        waypoints.append(self.__mini_games[-1].start_time + self.__mini_games[-1].life_time)
        return waypoints
