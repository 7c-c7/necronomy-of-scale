import pygame
import sys
import nos
import nos.config as config
import nos.desktop as desktop


class Necronomy:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Necronomy of Scale')
        self.screen = pygame.display.set_mode((config.WINDOW["width"], config.WINDOW["height"]))
        self.clock = pygame.time.Clock()
        self.groups = [nos.Group([desktop.Desktop()])]

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            for group in self.groups:
                group.draw(self.screen)
            pygame.display.update()
            self.clock.tick(config.WINDOW["fps"])


if __name__ == '__main__':
    Necronomy().run()
