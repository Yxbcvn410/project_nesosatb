class Level:
    def __init__(self, beat_size, bpm, music):
        self.beat_size = beat_size
        self.bpm = bpm
        self.music = music
        self.__mini_games = []
        self.overall_time = 0
        self.score = 0
        self.health_max = 1000
        self.health = self.health_max
        self.active_mini_game = None

    def add_mini_game(self, mini_game):
        """Добавляем мини-игру. По-другому добавлять мини-игры нельзя!"""
        self.__mini_games.append(mini_game)
        self.active_mini_game = self.__get_nearest_future_mini_game({'bars': 0})
        self.overall_time = max(self.overall_time, mini_game.start_time + mini_game.life_time)

    def __get_nearest_future_mini_game(self, time: dict):
        """Ищем ближайшую мини-игру в будущем"""
        nearest_mini_game = None
        for mini_game in self.__mini_games:
            if (mini_game.start_time >= time['bars']) and (
                    (nearest_mini_game is None) or (nearest_mini_game.start_time > mini_game.start_time)):
                nearest_mini_game = mini_game
        return nearest_mini_game

    def update(self, time: dict, graphical_ui):
        """Обновить текущую мини-игру и графическое представление"""
        if self.active_mini_game.is_over(time):
            # Текущая мини-игра закончилась, ищем следующую
            self.score += self.active_mini_game.score
            self.health -= self.active_mini_game.health_lost
            self.active_mini_game = self.__get_nearest_future_mini_game(time)

        if self.active_mini_game:
            # Если есть мини-игра в будущем, обновляем и рисуем
            minigame_time = dict(time)
            minigame_time['bars'] -= self.active_mini_game.start_time
            self.active_mini_game.update(minigame_time)
            self.active_mini_game.draw(minigame_time, graphical_ui)
            graphical_ui.draw_info({
                'current_score': self.active_mini_game.score,
                'global_score': self.score,
                'health_info': {'health': self.health, 'max': self.health_max},
                'progress': time['bars'] / self.overall_time
            })
            if self.health - self.active_mini_game.health_lost < 0:
                # Здоровье кончилось
                graphical_ui.draw_game_over({'score': self.score, 'health': self.health})
                self.active_mini_game = None
        else:
            # Уровень закончился, мини-игр больше нет
            graphical_ui.draw_game_over({'score': self.score, 'health': self.health})
        return {'over': self.active_mini_game is None, 'score': self.score}

    def handle_event(self, event):
        """Передать мини-игре событие нажатия"""
        if self.active_mini_game:
            event['time']['bars'] -= self.active_mini_game.start_time
            self.active_mini_game.handle(event)
        # То, как событие отобразится на графическом представлении, определяет мини-игра
