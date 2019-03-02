"""
pygame.event:
    事件模块
    class EventType:
        事件类型, 有一个最常用的属性type(int类型)，代表了事件的类型
        有哪些事件类型在pygame中定义的有，例如pygame.QUIT,
        某些事件还会有一些其他属性, 常用的事件列在下面:
        Event            Attribute
        QUIT             none
        ACTIVEEVENT      gain, state
        KEYDOWN          unicode, key, mod
        KEYUP            key, mod
        MOUSEMOTION      pos, rel, buttons
        MOUSEBUTTONUP    pos, button
        MOUSEBUTTONDOWN  pos, button
    get() -> Eventlist:
        一次性将事件队列中所有事件出队列，以列表形式返回
    wait() -> EventType instance:
        将事件出队列，如果队列为空，程序就阻塞住
    poll() -> EventType instance:
        将事件出队列，如果队列为空，就返回一个NOEVENT类型的事件
    set_blocked(type) -> None:
        禁止某些事件加入事件队列中(相当于不监听了), 可用于过滤事件
    set_allowed(type|typelist) -> None:
        设置某些事件允许加入队列中, 与set_block相对
"""
import pygame
from pygame.locals import *
from sys import exit


def testGet():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    while True:
        events = pygame.event.get()
        print(events)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        pygame.display.update()


def testWait():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    while True:
        event = pygame.event.wait()
        print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        pygame.display.update()


def testPoll():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    while True:
        event = pygame.event.poll()
        if event.type == pygame.NOEVENT:
            print('无事件发生')
        else:
            print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        pygame.display.update()


def testMouse():
    """鼠标事件

    MOUSEMOTION:
        鼠标移动事件
        pos: 到达位置
        rel: 移动向量
        buttons:
            一个三元组, 代表了左中右三个键的拖拽, 为1代表按下
            例如(1, 0, 0)代表按着鼠标左键拖拽
    MOUSEBUTTONDOWN|MOUSEBUTTONUP:
        鼠标点击事件
        pos: 位置
        button: 那个鼠标按键点下了, 1|2|3代表了左中右
    """
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        elif event.type == pygame.MOUSEMOTION:
            pos = event.pos
            rel = event.rel
            buttons = event.buttons
            print('鼠标位置:', pos, '移动:', rel, '移动中鼠标按键:', buttons)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('鼠标按下:', event.button, '位置:', event.pos)
        pygame.display.update()


def testKeyboard():
    """键盘事件测试

    KEYDOWN:
        unicode: str类型, 代表了按键对应的unicode字符, 如果无返回空字符串(如Shift)
        key: int类型, 按键的编码, pygame中有相关的常量定义, 如pygame.K_0
        mod: 如果 mod & pygame.KMOD_SHIFT 为 True，说明按了Shift组合键, 其他的同理
    KEYUP:
        key
        mod
    """
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        elif event.type == pygame.KEYDOWN:
            unic = event.unicode
            key = event.key
            mod = event.mod
            s1 = '按下了Key: {}, 对应的Unicode字符为<{}>'.format(key, unic)
            if mod & pygame.KMOD_SHIFT:
                s1 += ', 用户同时按了Shift组合键'
            print(s1)
        elif event.type == pygame.KEYUP:
            print(event.key, event.mod)
        pygame.display.update()


def testFilter():
    """使用block和allow进行事件过滤"""
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    # 不在监听鼠标移动事件
    pygame.event.set_blocked([pygame.MOUSEMOTION])
    while True:
        event = pygame.event.wait()
        print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        pygame.display.update()


def main():
    # testWait()
    testKeyboard()


if __name__ == "__main__":
    main()
