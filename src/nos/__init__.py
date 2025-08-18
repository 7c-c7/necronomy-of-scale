import typing

import pygame as pg

from nos import assets

COORDINATES = typing.TypeVar("COORDINATES", tuple[int | float, int | float], pg.Vector2)
TO_TOP = "to_top"
TO_BOTTOM = "to_bottom"


class Sprite(pg.sprite.Sprite):
    def __init__(
        self,
        asset: assets.Asset,
        rect: pg.Rect = None,
        position: COORDINATES = (0, 0),
        groups: list["Group"] = None,
    ):
        super().__init__(*(groups or []))
        self.image = asset.image
        self.rect = rect or self.image.get_rect()
        self.rect.topleft = position

    def process_event(self, event):
        return

    def update(self, *args, **kwargs):
        pass


class Animation:
    def __init__(
        self, images, img_duration: int | list[int] = 5, loop=True, initial_frame=0
    ):
        img_duration = (
            img_duration
            if isinstance(img_duration, list)
            else [img_duration for _ in images]
        )
        self.frames = images
        self.loop = loop
        self.img_duration = img_duration
        self.done = False
        self.frame = initial_frame
        self.frame_index = 0
        self.total_frames = sum(img_duration)
        self.end_frames = [img_duration[0] - 1]
        for i in range(1, len(img_duration)):
            self.end_frames.append(img_duration[i] + self.end_frames[i - 1])

    def copy(self):
        return Animation(self.frames, self.img_duration, self.loop)

    def advance(self, num_frames: int = 1):
        if self.loop:
            self.frame = (self.frame + num_frames) % self.total_frames
        else:
            self.frame = min(self.frame + num_frames, self.total_frames - 1)
            if self.frame >= self.total_frames - 1:
                self.done = True
        self.frame_index = (
            self.frame_index
            if self.frame < self.end_frames[self.frame_index]
            else (self.frame_index + 1) % len(self.frames)
        )

    @property
    def image(self):
        return self.frames[self.frame_index]

    def reset(self):
        self.frame = 0
        self.done = False


class AnimatedSprite(Sprite):
    def __init__(
        self,
        asset: assets.AnimatedAsset,
        initial_state: str = "idle",
        rect: pg.Rect = None,
        position: tuple[int, int] = (0, 0),
    ):
        super().__init__(asset, rect, position)
        self.asset = asset
        self.animations = asset.animations
        self._state: str = initial_state
        self.state = initial_state

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state: str):
        self._state = state
        self.animation = self.animations[self._state]
        self.animation.reset()
        self.image = self.animation.image

    def update(self, *_, **__):
        self.animation.advance()
        self.image = self.animation.image


class Group(pg.sprite.Group):
    def __init__(
        self,
        sprites: list[Sprite | typing.Self] = None,
        position_offset: tuple[int, int] = (0, 0),
    ):
        super().__init__(*sprites)
        self.position_offset = position_offset
        self.rect = self.bounding_rect()
        self.reorder = None

    def bounding_rect(self):
        rect = self.sprites()[0].rect.copy()
        for sprite in self.sprites():
            rect.union_ip(sprite.rect)
        return rect

    def add(self, *sprites):
        super().add(*sprites)
        self.rect = self.bounding_rect()

    def remove(self, *sprites):
        super().remove(*sprites)
        self.rect = self.bounding_rect()

    def process_event(self, event):
        for sprite in self.sprites():
            sprite.process_event(event)

    def update(self, *args, **kwargs):
        for sprite in self.sprites():
            sprite.update(*args, **kwargs)


class Selectable:
    def __init__(
        self: Group | typing.Self, select_mask: Sprite = None, is_selected: bool = False
    ):
        self.is_selected = is_selected
        self.reorder = getattr(self, "reorder", None)
        self.select_mask = select_mask
        if not self.select_mask:
            border_surface = pg.Surface(
                (self.rect.width, self.rect.height), pg.SRCALPHA
            )
            pg.draw.rect(
                border_surface,
                (255, 0, 0),
                [0, 0, self.rect.width - 1, self.rect.height - 1],
                1,
            )
            self.select_mask = Sprite(
                assets.Asset(spritesheet=border_surface), position=self.rect.topleft
            )

    def process_event(self: Group | typing.Type[typing.Self], event):
        super_safe(super(), "process_event", event)
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.select()
                return True
            else:
                self.deselect()
                return False

    def select(self: Group | typing.Type[typing.Self]):
        self.is_selected = True
        self.add(self.select_mask)
        self.reorder = TO_TOP

    def deselect(self: Group | typing.Type[typing.Self]):
        self.is_selected = False
        self.remove(self.select_mask)

    def toggle_select(self):
        self.select() if not self.is_selected else self.deselect()

    def update(self: type[Group] | typing.Self, *_, **__):
        super_safe(super(), "update")
        self.select_mask.rect.topleft = self.rect.topleft


class Draggable(Selectable):
    def __init__(
        self: Group | typing.Type[typing.Self],
        select_mask: Sprite = None,
        is_selected: bool = False,
    ):
        super().__init__(select_mask, is_selected)
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self._original_position = None
        self.reorder = getattr(self, "move", None)

    def process_event(self: Group | typing.Type[typing.Self], event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self._original_position = self.rect.topleft
                self.dragging = True
                mouse_x, mouse_y = event.pos
                self.offset_x = self.rect.x - mouse_x
                self.offset_y = self.rect.y - mouse_y
                self.reorder = TO_TOP
                return True
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
            return super().process_event(event)
        elif event.type == pg.MOUSEMOTION and self.dragging:
            mouse_x, mouse_y = event.pos
            self.rect.x = mouse_x + self.offset_x
            self.rect.y = mouse_y + self.offset_y
            return True


def super_safe(super_, function_name: str, *args, **kwargs):
    if super_function := getattr(super_, function_name, None):
        super_function(*args, **kwargs)
