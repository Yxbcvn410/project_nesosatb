from Engine.Interface import AbstractUI
from Engine.Level import LevelRuntime


class GameUI(AbstractUI):
    def __init__(self, canvas, runtime: LevelRuntime = None):
        super().__init__(canvas)
        self.runtime = runtime

    def key_press(self, key):
        if (key != 'p') or not self.runtime:
            self.runtime.key_pressed(key)
            return

        if self.runtime.paused:
            self.runtime.play()
        else:
            self.runtime.pause()

    def draw_widgets(self):
        pass  # TODO

    def set_info(self, info: dict):
        pass  # TODO

    def game_over(self, game_stats: dict):
        pass  # TODO
