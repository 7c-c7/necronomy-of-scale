import sys

import pygame
import pygame_gui as gui

import nos
import nos.assets as assets
import nos.config as config
import nos.workspace.cards as cards
import nos.workspace.desktop as desktop
import nos.workspace.manifest as manifest


class Necronomy:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Necronomy of Scale")
        self.screen = pygame.display.set_mode(
            (config.WINDOW["width"], config.WINDOW["height"])
        )
        self.clock = pygame.time.Clock()
        self.gui_manager = gui.UIManager(
            (config.WINDOW["width"], config.WINDOW["height"]),
            "assets/themes/pygame_gui_theme.json",
        )

        assets.initialize()

        self.skeletons = [
            cards.Card(
                assets.minions.SKELETON_ARCHER,
                position=(100, 100 + i * 65),
                card_data={"name": f"Archer {state}", "cost": 1},
                initial_state=state,
            )
            for i, state in enumerate(assets.minions.SKELETON_ARCHER.animation_tiles)
        ] + [
            cards.Card(
                assets.minions.SKELETON_SWORDSMAN,
                position=(400, 100 + i * 65),
                card_data={"name": f"Swordsman {state}", "cost": 1},
                initial_state=state,
            )
            for i, state in enumerate(assets.minions.SKELETON_SWORDSMAN.animation_tiles)
        ]

        self.workspace = nos.Group(
            [
                desktop.Desktop(),
                manifest.Manifest(self, self.gui_manager, self.skeletons),
            ]
        )

        self.groups = [
            self.workspace,
            *self.skeletons,
        ]

    def run(self):
        while True:
            time_delta = self.clock.tick(config.GAME["fps"]) / 1000.0
            for event in pygame.event.get():
                for group in self.groups:
                    if group.process_event(
                        event
                    ):  # If the event was fully handled, stop checking.
                        break
                if event.type == pygame.QUIT:
                    self.quit()

            for group in self.groups:
                group.update(time_delta)

            for group in self.groups:
                group.draw(self.screen)
            self.gui_manager.draw_ui(self.screen)
            pygame.display.flip()

    @staticmethod
    def quit(close=True):
        pygame.quit()
        if close:
            sys.exit()


if __name__ == "__main__":
    Necronomy().run()
