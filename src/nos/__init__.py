import pygame

from nos.config import WINDOW


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, rect: pygame.Rect = None, position: tuple[int, int] = (0, 0)):
        super().__init__()
        self.image = image
        self.rect = rect or self.image.get_rect()
        self.rect.topleft = position


class Group(pygame.sprite.Group):
    def __init__(self, sprites: list[Sprite] = None, position_offset: tuple[int, int] = (0, 0), ):
        super().__init__(*sprites)
        self.position_offset = position_offset
