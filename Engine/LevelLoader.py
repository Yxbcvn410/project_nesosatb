import json
import os

from Engine.Level import Level
from Engine.MiniGame import MiniGameWrapper
from MiniGames.LetaMiniGame import LetaMiniGame
from MiniGames.StubMinigame import StubMinigame
from MiniGames.VetaMinigame import VetaMiniGame


# Загружает конфигурацию уровня
# Формат конфигурации:
# 'bpm' - скорость уровня
# 'metadata' - метаданные уровня
# 'game' - данные игры

class LevelLoader:
    def __init__(self):
        self.levels = {}

    def scan_directory(self, directory: str):
        """Просканировать директорию и загрузить из неё все уровни"""
        if directory.endswith('/'):
            directory = directory[:-1]
        config_paths = [directory + '/' + file for file in os.listdir(directory) if '.json' in file]
        for config_path in config_paths:
            self.levels.update({len(self.levels): json.load(config_path)})

    def get_levels_metadata(self):
        """Возвращает метаданные всех уровней. Формат: {_id_: _metadata_}"""
        levels_metadata = {}
        for level_id in self.levels:
            levels_metadata.update({level_id: self.levels[level_id]['metadata'].copy()})
        return levels_metadata

    def load_level(self, level_id):
        """Загружает уровень по номеру"""
        if level_id in self.levels:
            level = Level(self.levels[level_id]['bpm'], metadata=self.levels[level_id]['metadata'])
            game = MiniGameWrapper()
            accessible_constructors = {
                'StubMiniGame': lambda life_time: StubMinigame(life_time),
                'LetaMiniGame': lambda life_time: LetaMiniGame(life_time),
                'VetaMiniGame': lambda life_time: VetaMiniGame(life_time)
            }
            game.configure(self.levels[level_id]['game'], accessible_constructors)
            level.load(game)
            return level
        raise ValueError()  # Нет уровня с таким ИД