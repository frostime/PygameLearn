"""
动画专题
实际上，在之前我们已经用到过动画方面的概念了，在Font.py里展示过
所谓动画，就是不停的blit，blit的内容按照时间发生变化

但是存在一个问题，那就是动画的帧率FPS（Frame Per Second）无法控制
有一个解决上述问题的方法，就是让我们的动画基于时间运作，我们需要知道上一个画面到现在经过了多少时间，然后我们才能决定是否开始绘制下一幅。
pygame.time模块给我们提供了一个Clock的对象，使我们可以轻易地控制FPS

注: 一般的电视画面是24FPS；30FPS基本可以给玩家提供流程的体验了；LCD的话，60FPS是常用的刷新率，游戏的帧率再高也就没什么意义了.


pygame.time：
    wait(milliseconds) -> time
    delay(milliseconds) -> time
        进程等待一段时间，不一定精确，所以会返回实际的等待时间
        后者比前者更加精确
    class Clock:
        Clock() -> Clock
        tick(framerate=0) -> milliseconds
            这个方法应该每帧调用一次, 它将计算自上次调用以来已经过了多少毫秒
            如果传递可选的framerate参数，该函数将延迟使游戏运行速度低于给定的帧率, 即限制游戏的运行速度
            比如通过每帧调用Clock.tick(40)一次，程序永远不会以每秒40帧以上的速度运行
        get_fps() -> float:
            计算FPS(桢/秒), 计算方式是计算前10次tick结果的平均值
"""
import pygame
from pygame.locals import *


def animation(FPS=30, moveSpeed=100):
    """
    绘制动画，控制帧数和物体移动的速度
    FPS, 移动速度 moveSpeed pixel/s
    """
    fontPath = r'C:\Windows\Fonts\SIMKAI.ttf'
    pygame.init()
    background = pygame.image.load(r'./Image/sushiplate.jpg')
    size = (640, 480)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('FPS')
    font = pygame.font.Font(fontPath, 20)
    text = font.render('FPS ≈ {}'.format(FPS), True,
                       (0, 0, 0), (255, 255, 255))
    (w, h) = text.get_size()
    at = [0, 240 - h // 2]
    direct = moveSpeed
    clock = pygame.time.Clock()
    while True:
        timePassed = clock.tick(FPS)
        print('经过时间: {}, FPS: {}'.format(timePassed, clock.get_fps()))
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        x = at[0]
        # timePassed是ms，速度却以s为单位
        x += direct * timePassed / 1000
        if x < 0:
            direct = -direct
            x = 0
        elif x > (size[0] - w):
            direct = -direct
            x = (size[0] - w)
        at[0] = x
        screen.blit(background, (0, 0))
        screen.blit(text, at)
        pygame.display.update()


if __name__ == "__main__":
    animation(60, 100)
