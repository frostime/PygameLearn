"""
本节讨论pygame中事件的问题
首先会给出三种事件获取方式: get(), wait(), poll()的功能和区别
然后会演示一下鼠标和键盘事件的处理
最后讲一下用户自定义事件

pygame.event:
    事件模块
    class EventType:
        事件类型, 有一个最常用的属性type(int类型)，代表了事件的类型
        有哪些事件类型在pygame中定义的有，例如pygame.QUIT,
        某些事件还会有一些其他属性, 常用的事件列在下面:
        type             int    attr
        QUIT             12     none
        ACTIVEEVENT      1      gain, state
        KEYDOWN          2      unicode, key, mod
        KEYUP            3      key, mod
        MOUSEMOTION      4      pos, rel, buttons
        MOUSEBUTTONUP    5      pos, button
        MOUSEBUTTONDOWN  6      pos, button
        JOYAXISMOTION    7      joy, axis, value
        JOYBALLMOTION    8      joy, ball, rel
        JOYHATMOTION     9      joy, hat, value
        JOYBUTTONUP      11     joy, button
        JOYBUTTONDOWN    10     joy, button
        VIDEORESIZE      16     size, w, h
        VIDEOEXPOSE      17     none
        USEREVENT        24     code
    class Event:
        Event(type, dict) -> EventType instance
        Event(type, **attributes) -> EventType instance
        定义一个事件
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


def testDIYEvent():
    """
    自定义一个事件
    1. 使用Event定义一个事件, 注意type是一个int
    如果希望自定义一个type的话有必要设置为大于24的数字，以便于同pygame中定义过的区分
    2. 用pygame.event.post将event插入事件队列中
    3. 处理事件
    """
    pygame.init()
    EVNET1 = 25
    EVENT2 = 26
    event1 = pygame.event.Event(EVNET1, message="Bad cat!")
    event2 = pygame.event.Event(EVENT2, {'Val': 1})
    pygame.event.post(event1)
    pygame.event.post(event2)
    # 然后获得它
    for event in pygame.event.get():
        if event.type == EVNET1:
            print(event.message)
        elif event.type == EVENT2:
            print(event.Val)
    pygame.quit()


def eventVal():
    print(QUIT)
    print(ACTIVEEVENT)
    print(KEYDOWN)
    print(KEYUP)
    print(MOUSEMOTION)
    print(MOUSEBUTTONUP)
    print(MOUSEBUTTONDOWN)
    print(JOYAXISMOTION)
    print(JOYBALLMOTION)
    print(JOYHATMOTION)
    print(JOYBUTTONUP)
    print(JOYBUTTONDOWN)
    print(VIDEORESIZE)
    print(VIDEOEXPOSE)
    print(USEREVENT)


def main():
    # testWait()
    # eventVal()
    testDIYEvent()
    


if __name__ == "__main__":
    main()
