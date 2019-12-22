import pygame

from Engine.Interface import AbstractUI

WHITE = (255, 255, 255)
BLUE = (0, 0, 200)
GREEN = (0, 200, 0)
RED = (255, 30, 0)
BLACK = (0, 0, 0)

MARGIN = 40


class ExitConfirmation(AbstractUI):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.exit = False

    def key_press(self, event):
        if event['key'] == pygame.K_LEFT and not self.exit:
            self.exit = True

        if event['key'] == pygame.K_RIGHT and self.exit:
            self.exit = False

        if event['key'] == pygame.K_SPACE:
            if self.exit:
                exit(0)
            else:
                return 'CONTINUE'

    def update(self):
        pass

    def draw_widgets(self):
        size = self.canvas.get_size()
        center = [a / 2 for a in size]

        # Background
        pygame.draw.rect(self.canvas, RED, [0, center[1] - 85, size[0], 170])
        pygame.draw.rect(self.canvas, WHITE, [0, center[1] - 80, size[0], 160])
        pygame.draw.rect(self.canvas, BLACK, [0, center[1] - 75, size[0], 150])

        font = pygame.font.Font('Assets/Fonts/Patapon.ttf', 40)
        over_text = font.render('Really quit game?', 1, WHITE)
        yes_text = font.render('Yes', 1, WHITE)
        no_text = font.render('No', 1, WHITE)
        c = yes_text.get_rect(center=(center[0], center[1] + 40))
        if self.exit:
            pygame.draw.rect(self.canvas, RED, (center[0] - c[2] / 2 - 40, c[1], c[2], c[3]))
        else:
            pygame.draw.rect(self.canvas, RED, (center[0] - c[2] / 2 + 40, c[1], c[2], c[3]))
        self.canvas.blit(over_text, over_text.get_rect(center=(center[0], center[1] - 40)))
        self.canvas.blit(yes_text, (center[0] - c[2] / 2 - 40, c[1]))
        self.canvas.blit(no_text, (center[0] - c[2] / 2 + 40, c[1]))
