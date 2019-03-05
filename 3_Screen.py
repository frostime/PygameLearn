"""
pygame.display:
    set_mode(resolution=(0,0), flags=0, depth=0) -> Surface:
        flag参数设置显示的模式，有如下
        pygame.FULLSCREEN    create a fullscreen display
        pygame.DOUBLEBUF     recommended for HWSURFACE or OPENGL
        pygame.HWSURFACE     hardware accelerated, only in FULLSCREEN
        pygame.OPENGL        create an OpenGL-renderable display
        pygame.RESIZABLE     display window should be sizeable
        pygame.NOFRAME       display window will have no border or controls
        如果想要多种模式，使用 | 连接即可
"""
import pygame
from pygame.locals import *


def testFullscreen():
    """全屏显示
    按f11进入全屏，按esc退出全屏
    pygame.HWSURFACE会把画面放入显存中获得更好的体验，但必须和FUULSCREEN搭配使用
    """
    pygame.init()
    screen = pygame.display.set_mode(
        (640, 480), pygame.FULLSCREEN | pygame.HWSURFACE
    )
    background = pygame.image.load(r'./Image/sushiplate.jpg').convert()
    pygame.event.set_blocked([pygame.MOUSEBUTTONDOWN])
    while True:
        pygame.display.update()
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                screen = pygame.display.set_mode((640, 480))
            elif event.key == pygame.K_F11:
                screen = pygame.display.set_mode(
                    (640, 480), pygame.FULLSCREEN | pygame.HWSURFACE
                )
        elif event.type == pygame.QUIT:
            pygame.quit()
            return
        screen.blit(background, (0, 0))


def testResizable():
    pygame.init()
    SCREEN_SIZE = (640, 480)
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
    background = pygame.image.load(r'./Image/sushiplate.jpg').convert()
    pygame.event.set_blocked([pygame.MOUSEBUTTONDOWN])
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        elif event.type == VIDEORESIZE:
            SCREEN_SIZE = event.size
            # screen = pygame.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)
            pygame.display.set_caption("Window resized to "+str(event.size))
        screen.blit(background, (0, 0))
        # 这里需要重新填满窗口
        screen_width, screen_height = SCREEN_SIZE
        for y in range(0, screen_height, background.get_height()):
            for x in range(0, screen_width, background.get_width()):
                screen.blit(background, (x, y))
        pygame.display.update()


def main():
    testFullscreen()
    # testResizable()


if __name__ == '__main__':
    main()
