from Engine import Level

FPS = 60


class MusicPlayer:
    def __init__(self):
        self.music = None  # TODO

    def load(self, file):
        print('Loaded music from {}'.format(file))  # TODO

    def play(self):
        print('Playback started')  # TODO

    def pause(self):
        print('Playback paused')  # TODO


class LevelRuntime:
    def __init__(self, graphical_ui):
        self.level = None
        self.time = 0.
        self.paused = True
        self.music = MusicPlayer()
        self.graphical_ui = graphical_ui

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
            'beat_type': 0 if abs(beat_delta) > (0.5 / FPS) else 1 if beat_no % self.level.beat_size else 2
        }

    def update(self):
        """Обновить уровень"""
        if not self.paused:
            level_status = self.level.update(self.get_time_dict(), self.graphical_ui)
            if level_status['over']:
                self.level = None
                self.pause()
            self.time += 1 / FPS
            return level_status
        return {'over': not bool(self.level)}

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
            # Уровень не загружен!
            raise AssertionError
        self.music.play()
        self.paused = False

    def load(self, level: Level.Level):
        """Загрузить уровень"""
        self.level = level
        self.music.load(self.level.music)
