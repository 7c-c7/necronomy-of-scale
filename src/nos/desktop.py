import nos
from nos.assets import load_asset, DESKTOP


class Desktop(nos.Sprite):
    """
    The Desktop on which the necromancer will be able to manage their army.
    """
    def __init__(self):
        super().__init__(load_asset(DESKTOP), position=(0, 0))
