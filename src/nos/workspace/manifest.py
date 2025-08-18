import pygame as pg
import pygame_gui as gui

import nos
import nos.assets as assets
import nos.config as config
import nos.main as main
import nos.workspace
import nos.workspace.cards as nos_cards

POSITION = (
    config.GAME["manifest"]["edge_margin"],
    config.GAME["manifest"]["edge_margin"],
)


class Manifest(nos.Group):
    def __init__(
        self,
        necronomy: main.Necronomy,
        gui_manager: gui.UIManager,
        cards: list[nos_cards.Card] = None,
    ):
        self.necronomy = necronomy
        self.gui_manager = gui_manager
        self.cards = cards or []
        self.page = nos.Sprite(assets.base.MANIFEST, position=POSITION)
        self.ui = ManifestUI(self)
        super().__init__([self.page, self.ui])


class ManifestUI(nos.Group):
    def __init__(self, manifest: Manifest):
        self.manifest = manifest
        self.manifest_container = gui.elements.UIWindow(
            rect=self.manifest.page.rect,
            manager=self.manifest.gui_manager,
            visible=False,
        )
        self.relative_rect = pg.Rect((0, 0), (100, 50))
        self.relative_rect.bottomright = (-50, -50)
        self.heal_all = gui.elements.UIButton(
            relative_rect=self.relative_rect,
            text="Heal All",
            manager=self.manifest.gui_manager,
            anchors={"right": "right", "bottom": "bottom"},
            visible=True,
            container=self.manifest_container,
            command={
                gui.UI_BUTTON_PRESSED: lambda *_: print(
                    " Healed.\n".join(
                        [card.card_data["name"] for card in self.manifest.cards] + [""]
                    )
                )
            },
        )
        super().__init__([self.heal_all])  # type: ignore
