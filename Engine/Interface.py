import abc
import time


class AbstractUI(abc.ABC):
    @abc.abstractmethod
    def __init__(self, canvas):
        self.canvas = canvas
        self.runtime = None
        self.views = None

    def load_ui_context(self, views: dict):
        """Загружаем возможные интерфейсы для перехода. Каждый элемент - пара (UI, runtime)"""
        self.views = views

    def set_runtime(self, runtime):
        """Runtime - объект, контролирующий выполнение. Можно в него вынести обработку нажатия."""
        self.runtime = runtime

    @abc.abstractmethod
    def key_press(self, event):
        """Обработать нажатие клавиши. Возвращать новое представление (Экземпляр AbstractUI) если его нужно изменить."""
        pass

    @abc.abstractmethod
    def update(self):
        """Обновляется, обновляет рантайм если есть. Вызывается синхронно с FPS."""
        pass

    @abc.abstractmethod
    def draw_widgets(self):
        """Рисует на экране виджеты."""
        pass

    def clean_canvas(self):
        """Очищает холст"""
        self.canvas.fill((0, 0, 0))


class AnimationRuntime:
    def __init__(self):
        self.animations = []

    def add_animation(self, sprite, animation_time, final_state: dict, time_offset=0.):
        if 'center' in final_state:
            center = final_state.pop('center')
            final_state.update({'x': center[0], 'y': center[1]})
        updated_final_state = sprite.get_property(number_only=True)
        updated_final_state.update(final_state)
        self.animations.append(
            {'sprite': sprite, 'start_time': time.time() + time_offset, 'transition_time': animation_time,
             'start_state': sprite.get_property(number_only=True), 'final_state': updated_final_state})

    def add_animation_by_keyframes(self, sprite, keyframes):
        if 0 in keyframes:
            sprite.transform(keyframes[0])
            keyframes.pop(0)
        processed_time = 0
        for key in keyframes:
            self.add_animation(sprite, key - processed_time, keyframes[key], processed_time)
            processed_time = key

    def update_all(self, surface):
        i = 0
        while i < len(self.animations):
            animation = self.animations[i]
            current_time = time.time()
            sprite = animation['sprite']
            if animation['start_time'] > current_time:  # Анимация ещё не началась
                animation['start_state'] = sprite.get_property(number_only=True)
                i += 1
                continue
            if animation['start_time'] + animation['transition_time'] < current_time:  # Уже кончилась
                sprite.transform(**(animation['final_state']))
                self.animations.pop(i)
                continue
            progress = (current_time - animation['start_time']) / (animation['transition_time'])
            kwargs = dict.fromkeys(sprite.get_property(number_only=True))
            for key in kwargs:
                kwargs[key] = animation['start_state'][key] * (1 - progress) + animation['final_state'][key] * progress
            sprite.transform(**kwargs)
            sprite.draw(surface)
            i += 1

    def delete_animation(self, sprite):
        sprites = [animation['sprite'] for animation in self.animations]
        if sprite in sprites:
            return self.animations.pop(sprites.index(sprite))['final_state']

    def delete_all_animations(self):
        self.animations.clear()

    def is_animating(self) -> bool:
        return bool(self.animations)
