# -*- coding: utf-8 -*-
"""
基于pygame的生命游戏
"""
import pygame
import sys
import numpy as np
import time


class Game(object):
    def __init__(self, screenSize, grids=(10, 10), FPS=40):
        self.size = screenSize
        self.screen = pygame.display.set_mode(screenSize)
        pygame.display.set_caption('生命游戏')
        self.initWidgets(grids)
        self.FPS = FPS
        self.clock = pygame.time.Clock()

    def initWidgets(self, grids):
        self.r = grids[0]
        self.c = grids[1]
        self.grids = np.zeros(grids, dtype=int)
        self.gridSize = (self.size[0] // grids[0], self.size[1] // grids[1])

    def run(self):
        pygame.init()
        self.draw()
        while True:
            self.dt = self.clock.tick(self.FPS) / 1000
            self.event()
            self.update()
            self.draw()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()

    def update(self):
        dup = self.grids.copy()
        for (i, j), v in np.ndenumerate(self.grids):
            alive = self.surround(i, j)
            if alive == 3:
                dup[i, j] = 1
            elif alive == 2:
                pass
            else:
                dup[i, j] = 0
        self.grids = dup

    def surround(self, i, j):
        sur = [
            (i-1, j-1), (i-1, j), (i-1, j+1),
            (i, j-1), (i, j+1),
            (i+1, j-1), (i+1, j), (i+1, j+1)
        ]
        alive = 0
        for r, c in sur:
            if r < 0 or r >= self.r or c < 0 or c >= self.c:
                continue
            else:
                if self.grids[r, c] == 1:
                    alive += 1
        return int(alive)

    def exit(self):
        pygame.quit()
        sys.exit()

    def draw(self):
        for (i, j), v in np.ndenumerate(self.grids):
            if v == 0:
                color = (255, 255, 255)
            else:
                color = (0, 0, 0)
            rect = self.index2Rect(i, j)
            pygame.draw.rect(self.screen, color, rect)
        pygame.display.update()

    def index2Rect(self, i, j):
        left = j * self.gridSize[0]
        top = i * self.gridSize[1]
        return (left, top, self.gridSize[0], self.gridSize[0])


def randomInit(game, initRate=0.4):
    grids = game.grids
    for (i, j), _ in np.ndenumerate(grids):
        r = np.random.rand()
        if r <= initRate:
            grids[i, j] = 1


def oneByOneInit(game):
    grids = game.grids
    l = 0
    m, n = np.shape(grids)
    for i in range(m):
        k = l
        for j in range(n):
            if k % 2 == 0:
                x = 0
            else:
                x = 1
            grids[i, j] = x
            k += 1
        l = 1 if l == 0 else 0


def crossInit(game, width=20):
    grids = game.grids
    m, n = np.shape(grids)
    center = (m // 2, n // 2)
    for i in range(m):
        for j in range(center[0] - width // 2, center[0] + width // 2 + 1):
            grids[i, j] = 1
    for i in range(n):
        for j in range(center[0] - width // 2, center[0] + width // 2 + 1):
            grids[j, i] = 1


def byHandInit(game):
    grids = game.grids
    grids[0, 1] = 1
    grids[1, 2] = 1
    grids[2, 0] = 1
    grids[2, 1] = 1
    grids[2, 2] = 1


def main():
    game = Game((720, 720), (180, 180), FPS=10)
    # randomInit(game, 0.1)
    oneByOneInit(game)
    # crossInit(game, 40)
    # game = Game((720, 720), (72, 72), FPS=20)
    # byHandInit(game)
    game.run()


if __name__ == '__main__':
    main()
