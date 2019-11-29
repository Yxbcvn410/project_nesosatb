class Level:
    def __init__(self, beat_size, bpm, music):
        self.beat_size = beat_size
        self.bpm = bpm
        self.music = music
        self.__mini_games = []
        self.score = 0
        self.active_mini_game = None

    def add_mini_game(self, mini_game):
        self.__mini_games.append(mini_game)
        self.active_mini_game = self.__get_nearest_future_mini_game({'bars': 0})

    def __get_nearest_future_mini_game(self, time: dict):
        nearest_mini_game = None
        for mini_game in self.__mini_games:
            if (mini_game.start_time >= time['bars']) and (
                    (nearest_mini_game is None) or (nearest_mini_game.start_time > mini_game.start_time)):
                nearest_mini_game = mini_game
        return nearest_mini_game

    def update(self, time: dict):
        if not self.active_mini_game:
            return {'over': True, 'score': self.score}
        elif self.active_mini_game.is_over(time):
            self.score += self.active_mini_game.score
            self.active_mini_game = self.__get_nearest_future_mini_game(time)

        if self.active_mini_game:
            self.active_mini_game.update(time)
            self.active_mini_game.draw(time, None)  # TODO add GUI
        return {'over': self.active_mini_game is None, 'score': self.score}

    def handle_event(self, event):
        self.active_mini_game.handle(event)
