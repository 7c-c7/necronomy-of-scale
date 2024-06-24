from __future__ import annotations

import pygame as pg
from pathlib import Path

DESKTOP = Path('assets/desktop.png')


def load_asset(path: Path) -> pg.Surface:
    return pg.image.load(path).convert()
