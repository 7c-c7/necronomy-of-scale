import pygame as pg

import nos
import nos.assets as assets


POSITION = (5, 5)


class Manifest(nos.Sprite):
    def __init__(self):
        super().__init__(assets.MANIFEST.convert(), position=POSITION)
