import nos
from nos.assets import load_asset, DESKTOP
import nos.manifest as manifest


class Desktop(nos.Sprite):
    """
    The Desktop on which the necromancer will be able to manage their army.
    """

    def __init__(self):
        super().__init__(DESKTOP.convert(), position=(0, 0))
        self.manifest = manifest.Manifest()
