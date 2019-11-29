from Engine.AbstractMinigame import *
import sys


class StubMinigame(AbstractMiniGame):
    def __init__(self, start_time, life_time):
        super().__init__(start_time, life_time)

    def update(self, time: dict):
        pass

    def draw(self, time: dict, graphical_ui):
        if time['bars'] < self.start_time:
            return
        if time['beat_type']:
            sys.stdout.write('strong beat\n' if time['beat_type'] == 2 else 'beat\n')
            sys.stdout.flush()

    def handle(self, event):
        sys.stdout.write(str(event) + '\n')
        sys.stdout.flush()
