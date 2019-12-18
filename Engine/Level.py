import pygame

from Engine.Media import MusicPlayer

FPS = 30


class Level:
    def __init__(self, beat_size, bpm, music, graphical_ui, health_max=1000):
        self.beat_size = beat_size
        self.bpm = bpm
        self.music = music
        self.graphical_ui = graphical_ui
        self.game = None
        self.health_max = health_max
        self.health = health_max
        self.score = 0
        self.progress = 0.

    def load(self, wrapper):
        self.game = wrapper

    def update(self, time: dict):
        """Обновить текущую мини-игру и графическое представление
        Возврат True если игра закончена, иначе False"""
        self.progress = time['bars'] / self.game.life_time
        game_states_change = self.game.update(time)
        self.health -= game_states_change['delta_health']
        self.score += game_states_change['delta_score']
        return not self.game.is_over(time) and (self.health > 0)

    def draw(self, time: dict):
        self.game.draw(time, self.graphical_ui)

    def handle_event(self, event):
        """Передать мини-игре событие нажатия"""
        game_states_change = self.game.handle(event)
        self.health -= game_states_change['delta_health']
        self.score += game_states_change['delta_score']
        # То, как событие отобразится на графическом представлении, определяет мини-игра

    def get_stats(self):
        return {
            'current_score': self.score,
            'global_score': self.score,
            'health_info': {'health': self.health, 'max': self.health_max},
            'progress': self.progress
        }


class LevelRuntime:
    def __init__(self):
        self.level = None
        self.time = 0.
        self.paused = True
        self.music = MusicPlayer()

    def get_time_dict(self):
        """Получить расширенную информацию о текущем времени"""
        beat_no = int(self.time * self.level.bpm / 60)
        beat_delta = self.time - beat_no * (60 / self.level.bpm)
        if beat_delta > 30 / self.level.bpm:
            beat_delta = beat_delta - 60 / self.level.bpm
            beat_no += 1
        return {
            'bars': beat_no // self.level.beat_size,
            'beats': beat_no % self.level.beat_size,
            'delta': beat_delta * self.level.bpm / 60,
            'beat_type':
                -1 if beat_delta - (30 / self.level.bpm) > - 1 / FPS
                else 0 if abs(beat_delta) > (0.5 / FPS)
                else 1 if beat_no % self.level.beat_size
                else 2
        }

    def update(self):
        """Обновить уровень. Возвращает True если выполняется, иначе False"""
        level_over = False
        if not self.paused:
            self.time += 1 / FPS
            level_over = self.level.update(self.get_time_dict())
        self.level.draw(self.get_time_dict())
        return {'pause': self.paused, 'over': level_over, 'stats': self.level.get_stats()}

    def key_pressed(self, key):
        """Обработать нажатие клавиши"""
        if not self.paused:
            self.level.handle_event({'key': key, 'time': self.get_time_dict()})

    def pause(self):
        """Поставить уровень на паузу"""
        self.music.pause()
        self.paused = True

    def play(self):
        """Запустить уровень (После загрузки или паузы)"""
        if self.level is None:
            raise AssertionError  # Уровень не загружен!
        self.music.play()
        self.paused = False

    def load(self, level: Level):
        """Загрузить уровень"""
        self.level = level
        self.music.load(self.level.music)
