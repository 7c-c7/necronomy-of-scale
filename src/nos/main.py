import pygame
import sys
import nos
import nos.config as config
import nos.desktop as desktop
from nos import cards, assets


class Necronomy:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Necronomy of Scale")
        self.screen = pygame.display.set_mode(
            (config.WINDOW["width"], config.WINDOW["height"])
        )
        self.clock = pygame.time.Clock()
        assets.initialize()

        self.skeletons = [
            cards.Card(
                assets.SKELETON_ARCHER,
                position=(100, 100 + i * 65),
                card_data={"name": f"Archer {state}", "cost": 1},
                initial_state=state,
            )
            for i, state in enumerate(assets.SKELETON_ARCHER.animation_tiles)
        ] + [
            cards.Card(
                assets.SKELETON_SWORDSMAN,
                position=(400, 100 + i * 65),
                card_data={"name": f"Swordsman {state}", "cost": 1},
                initial_state=state,
            )
            for i, state in enumerate(assets.SKELETON_SWORDSMAN.animation_tiles)
        ]

        self.groups = [
            nos.Group([desktop.Desktop(), desktop.manifest.Manifest()]),
            *self.skeletons,
        ]

    def run(self):
        while True:
            for event in pygame.event.get():
                for group in reversed(self.groups):
                    if group.handle_event(
                        event
                    ):  # If the event was fully handled, stop checking.
                        break
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            for group in self.groups:
                group.update()

            for group in self.groups:
                group.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(config.GAME["fps"])


if __name__ == "__main__":
    Necronomy().run()
