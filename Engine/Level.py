import time

import pygame


class Level:
    def __init__(self, bpm, health_max=100, metadata={}):
        self.bpm = bpm
        self.game = None
        self.health_max = health_max
        self.health = health_max
        self.score = 0
        self.progress = 0.
        self.__metadata = metadata
        if 'empty_bars' not in self.__metadata:
            self.__metadata.update({'empty_bars': 1})

    def load(self, wrapper):
        self.game = wrapper

    def get_beat_size(self):
        return self.game.beat_size

    def update(self, time_dict: dict):
        """Обновить текущую мини-игру
        Возврат True если игра закончена, иначе False"""
        time_dict['bars'] -= self.__metadata['empty_bars']
        if time_dict['bars'] < 0:
            self.progress = (self.__metadata['empty_bars'] + time_dict['bars'] + (
                    time_dict['beats'] + time_dict['delta'] + 0.5) /
                             time_dict['beat_size']) / (self.game.life_time + self.__metadata['empty_bars'])
            return False
        is_level_over = self.game.is_over(time_dict) or self.health <= 0
        if not is_level_over:
            self.progress = (self.__metadata['empty_bars'] + time_dict['bars'] + (
                    time_dict['beats'] + time_dict['delta'] + 0.5) /
                             time_dict['beat_size']) / (self.game.life_time + self.__metadata['empty_bars'])
            game_states_change = self.game.update(time_dict)
            self.score += game_states_change['delta_score']
            self.health += game_states_change['delta_health']
            if self.health < 0:  # Здоровье меньше нуля - не тема. Зомби не нужны.
                self.health = 0
            if self.health > self.health_max:  # Больше максимума - тоже не тема
                self.health = self.health_max
        elif self.progress > 1:
            self.progress = 1
        return is_level_over

    def draw(self, canvas, time_dict: dict):
        time_dict['bars'] -= self.__metadata['empty_bars']
        if time_dict['bars'] < 0:
            return
        self.game.draw(time_dict, canvas)

    def handle_event(self, event):
        """Передать мини-игре событие нажатия"""
        event['time']['bars'] -= self.__metadata['empty_bars']
        if event['time']['bars'] < 0:
            return
        game_states_change = self.game.handle(event)
        self.health += game_states_change['delta_health']
        self.score += game_states_change['delta_score']
        if self.health < 0:
            self.health = 0
        if self.health > self.health_max:
            self.health = self.health_max

    def get_stats(self):
        return {
            'current_score': int(self.game.current_mini_game_score),
            'global_score': int(self.score),
            'health_info': {'health': self.health, 'max': self.health_max},
            'progress': self.progress
        }

    def get_metadata(self):
        return self.__metadata.copy()

    def reset(self):
        self.score = 0
        self.progress = 0.
        self.health = self.health_max
        self.game.reset()

    def get_waypoints(self):
        return [(wp + self.__metadata['empty_bars']) / (self.game.life_time + self.__metadata['empty_bars']) for wp in
                self.game.get_waypoints()]


class LevelRuntime:
    def __init__(self):
        self.level = None
        self.active_time = 0.
        self.last_upd_time = time.time()
        self.dt = 0.
        self.paused = True
        self.music = False
        self.music_start_flag = False

    def get_time_dict(self):
        """Получить расширенную информацию о текущем времени"""
        beat_no = int(self.active_time * self.level.bpm / 60)
        beat_delta = self.active_time - beat_no * (60 / self.level.bpm)
        if beat_delta > 30 / self.level.bpm:
            beat_delta = beat_delta - 60 / self.level.bpm
            beat_no += 1
        return {
            'bars': beat_no // self.level.get_beat_size(),
            'beats': beat_no % self.level.get_beat_size(),
            'beat_size': self.level.get_beat_size(),
            'delta': beat_delta * self.level.bpm / 60,
            'beat_type':
                -1 if beat_delta - self.dt < -0.5 < beat_delta
                else 0 if not self.dt > beat_delta > 0
                else 1 if beat_no % self.level.get_beat_size()
                else 2
        }

    def update(self):
        """Обновить уровень. Возвращает True если выполняется, иначе False"""
        level_over = False
        if not self.paused:
            self.dt = time.time() - self.last_upd_time
            self.active_time += self.dt
            self.last_upd_time = time.time()
            level_over = self.level.update(self.get_time_dict())
        return {'pause': self.paused, 'over': level_over, 'stats': self.level.get_stats()}

    def key_pressed(self, key):
        """Обработать нажатие клавиши"""
        if not self.paused:
            self.level.handle_event({'key': key, 'time': self.get_time_dict()})

    def draw(self, canvas):
        self.level.draw(canvas, self.get_time_dict())

    def pause(self):
        """Поставить уровень на паузу"""
        if self.music:
            pygame.mixer.music.pause()
        self.paused = True

    def play(self):
        """Запустить уровень (После загрузки или паузы)"""
        if self.level is None:
            raise AssertionError  # Уровень не загружен!
        if self.music:
            if self.music_start_flag:
                pygame.mixer.music.unpause()
            else:
                self.music_start_flag = True
                pygame.mixer.music.play()
        self.paused = False
        self.last_upd_time = time.time()

    def load(self, level: Level):
        """Загрузить уровень"""
        self.level = level
        if 'music' in level.get_metadata():
            self.music = True
            pygame.mixer.music.load(level.get_metadata()['music'])
            if 'music_offset' in level.get_metadata():
                self.active_time = level.get_metadata()['music_offset']
