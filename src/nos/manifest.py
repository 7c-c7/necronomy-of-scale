import nos
import nos.assets.base as base_assets

POSITION = (5, 5)


class Manifest(nos.Sprite):
    def __init__(self):
        super().__init__(base_assets.MANIFEST, position=POSITION)
