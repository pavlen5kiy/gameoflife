import pygame
from load_image import load_image


class Sprite(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)


class Button(Sprite):
    def __init__(self, screen, screen_size, image, pos=(0, 0),
                 *group):
        super().__init__(*group)
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.orig = load_image(image)
        self.rect.topleft = pos
        self.orig_pos = pos
        self.hl = load_image(image + '_hl')
        self.screen = screen

    def update(self, *args):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.x <= mouse_pos[
            0] <= self.rect.x + self.orig.get_width() and self.rect.y <= \
                mouse_pos[1] <= self.rect.y + self.orig.get_height():
            self.image = self.hl
        else:
            self.image = self.orig

        if (args and args[0].type == pygame.MOUSEBUTTONDOWN and
                self.rect.collidepoint(args[0].pos)):
            return True

        return False

    def change_image(self, image):
        self.image = load_image(image)
        self.orig = load_image(image)
        self.hl = load_image(image + '_hl')


class Ui:
    def __init__(self, screen, screen_size):
        self.screen = screen
        self.width = screen_size[0]
        self.height = screen_size[1]


class Text(Ui):
    def __init__(self, screen, screen_size, font_size, color='white',
                 pos=(0, 0), center_align=True, right_align=False):
        super().__init__(screen, screen_size)
        self.font = pygame.font.Font('freesansbold.ttf',
                                     font_size)
        self.pos = pos
        self.color = pygame.Color(color)
        self.center_align = center_align
        self.right_align = right_align

        self.render = self.font.render('', True, self.color).convert_alpha()
        self.rect = self.render.get_rect()

    def update(self, message):
        self.render = self.font.render(str(message), True, self.color).convert_alpha()
        self.rect = self.render.get_rect()
        if self.center_align:
            pos = (self.pos[0] - self.render.get_width() // 2,
                   self.pos[1] - self.render.get_height() // 2)
        elif self.right_align:
            pos = (self.pos[0] - self.render.get_width(),
                   self.pos[1] - self.render.get_height() // 2)
        else:
            pos = (self.pos[0],
                   self.pos[1] - self.render.get_height() // 2)
        self.screen.blit(self.render, pos)