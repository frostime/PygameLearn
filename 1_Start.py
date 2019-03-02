"""
pygame初体验
一般导入格式:
import pygame
from pygame.locals import *

最开始: pygame.init(), 初始化pygame,为使用硬件做准备
退出游戏: sys.exit()

pygame.display:
    访问显示设备相关
    https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode
    set_mode(resolution=(0,0), flags=0, depth=0) -> Surface:
        初始化screen, 返回一个Surface对象代表screen
    set_caption(title, icontitle) -> None:
        设置窗口的caption
    update(rectangle=None) -> None:
        更新画面，如果新绘图之后需要调用它

pygame.Surface:
    pygame object for representing images and screen
    blit(source, dest, area=None, special_flags = 0) -> Rect:
        在dest处绘制source(Surface)的内容, dist可以是一个pair代表source的左上角
    get_width() -> width
    get_height() -> height

pygame.image:
    图片模块
    load(filename) -> Surface:
        导入一个图像
"""
import pygame
from pygame.locals import *
from sys import exit


def init():
    pygame.init()
    width = 640
    height = 480
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Hello World!")
    background = pygame.image.load(r'./Image/sushiplate.jpg')
    cursor = pygame.image.load(r'./Image/fugu.png')
    return screen, background, cursor


def main():
    screen, background, cursor = init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        screen.blit(background, (0, 0))
        x, y = pygame.mouse.get_pos()
        x -= cursor.get_width() // 2
        y -= cursor.get_height() // 2
        screen.blit(cursor, (x, y))
        pygame.display.update()


if __name__ == "__main__":
    main()
