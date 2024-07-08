from pathlib import Path

import pygame as pg

import nos

import nos.assets as assets
from nos import config


class Card(nos.Draggable, nos.Group):
    def __init__(
        self,
        asset: assets.AnimatedAsset,
        initial_state: str = "idle",
        position=(0, 0),
        icon_offset=None,
        card_data=None,
        is_selected=False,
    ):
        handwriting = pg.font.Font(Path("assets/fonts/Grand9K_Pixel.ttf"), 10)
        handwriting.italic = True
        card_data = card_data or {}
        self.card_data = card_data
        self.card = nos.Sprite(assets.CARD, position=position)
        self.icon = nos.AnimatedSprite(
            asset, position=position, initial_state=initial_state
        )
        self.icon_offset = icon_offset or (
            config.GAME["card"]["left_sprite_margin"],
            (self.card.image.size[1] - self.icon.image.size[1]) // 2,
        )
        self.text_offset = (self.icon_offset[0] + self.icon.image.size[0], 10)
        self.text_surface = assets.Asset(
            spritesheet=handwriting.render(
                self.card_data.get("name", ""), True, pg.Color("black")
            )
        )
        self.text_surface.load()
        self.text = nos.Sprite(
            self.text_surface,
            position=pg.Vector2(position) + pg.Vector2(self.text_offset),
        )
        nos.Group.__init__(self, sprites=[self.card, self.icon, self.text])
        nos.Draggable.__init__(
            self,
            select_mask=nos.Sprite(assets.CARD_SELECT_BORDER, position=position),
            is_selected=is_selected,
        )

    def update(self):
        super().update()
        self.card.rect.topleft = self.rect.topleft
        self.card.update()
        self.icon.rect = pg.Vector2(self.rect.topleft) + pg.Vector2(self.icon_offset)
        self.icon.update()
        self.text.rect = pg.Vector2(self.rect.topleft) + pg.Vector2(self.text_offset)
        self.text.update()
