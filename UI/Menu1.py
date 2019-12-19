from Engine.Interface import AbstractUI
import pygame
import pygame.gfxdraw


class Menu(AbstractUI, pygame.sprite.Sprite):

    def __init__(self, canvas):
        super().__init__(canvas)
        # добавление фонарика
        self.player = pygame.sprite.Sprite()
        self.source_light = pygame.image.load("Assets/Artwork/flashlight_orange.png").convert_alpha(self.canvas)
        self.source_light = pygame.transform.scale(self.source_light,
                                                   (self.canvas.get_width()//4, self.canvas.get_height()//4))
        self.player.image = self.source_light
        self.player.rect = self.source_light.get_rect()
        self.player.rect.center = (self.canvas.get_width()//2,
                                   self.canvas.get_height() - self.player.image.get_height()//2)
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)

        # луч
        self.light_on = True
        self.ray = pygame.sprite.Sprite()


        self.ray.image = pygame.Surface((self.canvas.get_width(), self.canvas.get_height()), pygame.SRCALPHA)
        pygame.gfxdraw.filled_circle(self.ray.image,
                                     self.canvas.get_width()//2, self.canvas.get_height()//4,
                                     self.player.image.get_width()//2, (240, 184, 0))
        pygame.gfxdraw.filled_circle(self.ray.image,
                                    self.canvas.get_width() // 2, self.canvas.get_height() // 4,
                                     int(0.74*self.player.image.get_height()), (255, 248, 176))
        self.ray.rect = self.ray.image.get_rect()
        self.player_group.add(self.ray)



        # пустое место
        self.nothing = pygame.sprite.Sprite()
        self.nothing.image = pygame.Surface((0, 0), pygame.SRCALPHA)
        pygame.gfxdraw.filled_circle(self.ray.image, self.canvas.get_width()//2, self.canvas.get_height()//4, 0, (0, 0, 0))
        self.nothing.rect = self.nothing.image.get_rect()
        self.game_list = [self.nothing, self.nothing, self.nothing]
        self.n_center = 3
        self.icon_group = pygame.sprite.Group()
        self.icon_group.add(*self.game_list)
        self.turning = 0

    def key_press(self, event):
        if event.key == pygame.K_h or event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.turning = -1

        elif event.key == pygame.K_h or event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.turning = +1
        pass

    def update(self):

            if self.turning <40:
                for sprt in self.player_group.sprites():
                    sprt.image = pygame.transform.rotate(sprt.image, 1)
                self.player_group.update()
            else:
            for sprt in self.player_group.sprites():
                sprt.image = pygame.transform.rotate(sprt.image, 1)
            self.player_group.update()
    def draw_widgets(self):
        self.clean_canvas()
        self.player_group.draw(self.canvas)
        #self.icon_group.draw(self.canvas)

    def add_level(self, level):
        pass
