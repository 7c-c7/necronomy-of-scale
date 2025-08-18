import nos
import nos.assets.base as base_assets


class Desktop(nos.Sprite):
    """
    The Desktop on which the necromancer will be able to manage their army.
    """

    def __init__(self):
        super().__init__(base_assets.DESKTOP, position=(0, 0))
