import nos.assets as assets
import nos.assets.base as base
from nos import config

# Card, what most things of importance will be displayed on.
CARD_SPRITESHEET_POSITION_OFFSET = (1927, 1445)
CARD_SPRITESHEET_SIZE = (74, 21)
CARD_SCALE = config.GAME["card"]["height"] / CARD_SPRITESHEET_SIZE[1]
card_page = assets.Asset(
    spritesheet=base.PAGES,
    tile_size=CARD_SPRITESHEET_SIZE,
    offset=CARD_SPRITESHEET_POSITION_OFFSET,
)
card_border = assets.Asset(
    spritesheet=base.BORDERS,
    tile_size=CARD_SPRITESHEET_SIZE,
    offset=CARD_SPRITESHEET_POSITION_OFFSET,
)
CARD = assets.Asset.stack([card_page, card_border], scale=CARD_SCALE)
CARD_SELECT_BORDER_OFFSET = (1927, 1478)
CARD_SELECT_BORDER = assets.Asset(
    spritesheet=base.BORDERS,
    tile_size=CARD_SPRITESHEET_SIZE,
    offset=CARD_SELECT_BORDER_OFFSET,
    scale=CARD_SCALE,
)
