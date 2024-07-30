from __future__ import annotations

from pathlib import Path

import pygame as pg

import nos.assets as assets
import nos.config as config

DESKTOP = assets.Asset(
    Path("assets/desktop.png"),
)

# Manifest, the main page.
MANIFEST_SPRITESHEET_POSITION_OFFSET = (176, 1040)
MANIFEST_SPRITESHEET_PAGE_SIZE = (592, 464)
PAGES = pg.image.load("assets/pages.png")
BORDERS = pg.image.load("assets/borders.png")
manifest_page = assets.Asset(
    spritesheet=PAGES,
    tile_size=MANIFEST_SPRITESHEET_PAGE_SIZE,
    offset=MANIFEST_SPRITESHEET_POSITION_OFFSET,
)
manifest_border = assets.Asset(
    spritesheet=BORDERS,
    tile_size=MANIFEST_SPRITESHEET_PAGE_SIZE,
    offset=MANIFEST_SPRITESHEET_POSITION_OFFSET,
)
MANIFEST = assets.Asset.stack(
    [manifest_page, manifest_border],
    scale=(
        config.GAME["manifest"]["width"] / MANIFEST_SPRITESHEET_PAGE_SIZE[0],
        config.GAME["manifest"]["height"] / MANIFEST_SPRITESHEET_PAGE_SIZE[1],
    ),
)
