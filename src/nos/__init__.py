import typing

import pygame as pg

from nos.config import WINDOW


class Sprite(pg.sprite.Sprite):
    def __init__(
        self,
        image: pg.Surface,
        rect: pg.Rect = None,
        position: tuple[int, int] = (0, 0),
    ):
        super().__init__()
        self.image = image
        self.rect = rect or self.image.get_rect()
        self.rect.topleft = position

    def handle_event(self, event):
        pass


class Group(pg.sprite.Group):
    def __init__(
        self,
        sprites: list[Sprite | typing.Type[typing.Self]] = None,
        position_offset: tuple[int, int] = (0, 0),
    ):
        super().__init__(*sprites)
        self.position_offset = position_offset


class Selectable:
    def __init__(self: Sprite, border: pg.Surface = None, is_selected: bool = False):
        self.is_selected = is_selected
        self.border = border
        self._original_image = None
        self._selected_image = None
        if not hasattr(self, "image"):
            self.image = None

    def handle_event(self: Sprite | typing.Type[typing.Self], event):
        super_safe(super(), "handle_event", event)
        if event.type == pg.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                self.toggle_select()

    def select(self: Sprite | typing.Type[typing.Self]):
        self.is_selected = True
        if not self._original_image or not self._selected_image:
            self._original_image = self.image
            self._selected_image = self.image.copy()
            if not self.border:
                self.border = pg.Surface(
                    (self.rect.width, self.rect.height), pg.SRCALPHA
                )
                pg.draw.rect(
                    self.border,
                    (255, 0, 0),
                    [0, 0, self.rect.width - 1, self.rect.height - 1],
                    1,
                )
            self._selected_image.blit(self.border, (0, 0))
        self.image = self._selected_image

    def deselect(self: Sprite | typing.Type[typing.Self]):
        self.is_selected = False
        self.image = self._original_image

    def toggle_select(self):
        self.select() if not self.is_selected else self.deselect()

    def draw(self: Sprite | typing.Type[typing.Self], screen):
        screen.blit(self.image, self.rect.topleft)


class Draggable(Selectable):
    def __init__(self: Sprite | typing.Type[typing.Self], select_mask: pg.Surface = None, is_selected: bool = False):
        super().__init__(select_mask, is_selected)
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self._selected_state = self.is_selected
        self._original_position = None

    def handle_event(self: Sprite | typing.Type[typing.Self], event):
        super().handle_event(event)
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self._selected_state = self.is_selected
                self._original_position = self.rect.topleft
                self.dragging = True
                mouse_x, mouse_y = event.pos
                self.offset_x = self.rect.x - mouse_x
                self.offset_y = self.rect.y - mouse_y
        elif event.type == pg.MOUSEBUTTONUP:
            self.dragging = False
            if self.rect.topleft != self._original_position:
                self.toggle_select()
        elif event.type == pg.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x + self.offset_x
                self.rect.y = mouse_y + self.offset_y


def super_safe(super_, function_name: str, *args, **kwargs):
    if super_function := getattr(super_, function_name):
        super_function(*args, **kwargs)
