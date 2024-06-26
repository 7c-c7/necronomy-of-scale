from __future__ import annotations

import pygame as pg
from pathlib import Path

DESKTOP = pg.image.load(Path("assets/desktop.png"))
MANIFEST_SPRITESHEET_POSITION_OFFSET = (176, 1040)
MANIFEST_SPRITESHEET_PAGE_SIZE = (592, 464)
PAGES = pg.image.load("assets/pages.png")
BORDERS = pg.image.load("assets/borders.png")
MANIFEST = PAGES.subsurface(
    pg.Rect(MANIFEST_SPRITESHEET_POSITION_OFFSET, MANIFEST_SPRITESHEET_PAGE_SIZE)
)
MANIFEST.blit(
    pg.image.load("assets/borders.png").subsurface(
        pg.Rect(MANIFEST_SPRITESHEET_POSITION_OFFSET, MANIFEST_SPRITESHEET_PAGE_SIZE)
    ),
    (0, 0),
)
CARD_SPRITESHEET_POSITION_OFFSET = (1927, 1445)
CARD_SPRITESHEET_SIZE = (74, 21)
CARD_SIZE = (CARD_SPRITESHEET_SIZE[0]*3, CARD_SPRITESHEET_SIZE[1]*3)
CARD = PAGES.subsurface(
    pg.Rect(CARD_SPRITESHEET_POSITION_OFFSET, CARD_SPRITESHEET_SIZE)
)
CARD.blit(
    pg.image.load("assets/borders.png").subsurface(
        pg.Rect(CARD_SPRITESHEET_POSITION_OFFSET, CARD_SPRITESHEET_SIZE)
    ),
    (0, 0),
)
CARD = pg.transform.scale(CARD, (74 * 3, 21 * 3))
CARD_SELECT_BORDER_OFFSET = (1927, 1478)
CARD_SELECT_BORDER = BORDERS.subsurface(
    pg.Rect(CARD_SELECT_BORDER_OFFSET, CARD_SPRITESHEET_SIZE)
)
CARD_SELECT_BORDER = pg.transform.scale(CARD_SELECT_BORDER, CARD_SIZE)
SKELETON_ARCHER = pg.image.load("assets/Skeleton_Archer.png")
SKELETON = pg.transform.scale(
    SKELETON_ARCHER.subsurface(pg.Rect((67, 0), (25, 32))), (25, 32)
)


def load_asset(path: Path) -> pg.Surface:
    return pg.image.load(path).convert()
