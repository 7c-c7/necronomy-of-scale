import nos

import nos.assets as assets


class Card(nos.Draggable, nos.Sprite):
    def __init__(
        self,
        image,
        position=(0, 0),
        position_offset=None,
        card_data=None,
        is_selected=False,
    ):
        card_data = card_data or {}
        position_offset = position_offset or (10, (assets.CARD.height - image.height)//2)
        assets.CARD.convert()
        assets.CARD_SELECT_BORDER.convert()
        nos.Draggable.__init__(self, select_mask=assets.CARD_SELECT_BORDER.copy(), is_selected=is_selected)
        self.position_offset = position_offset
        self.card_data = card_data
        card = assets.CARD.copy()
        card.blit(image.convert(), position_offset)
        nos.Sprite.__init__(self, card, position=position)
