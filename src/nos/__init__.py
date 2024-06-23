import sys

import pygame

from nos.config import WINDOW


class Necronomy:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Necronomy of Scale')
        self.screen = pygame.display.set_mode((WINDOW["width"], WINDOW["height"]))

        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(WINDOW["fps"])


if __name__ == '__main__':
    Necronomy().run()
