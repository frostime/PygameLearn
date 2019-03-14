"""
精灵专题的延续: 冲撞
在游戏中经常涉及到物体的冲撞检验的问题，对此sprite模块中有一大堆方法

pygame.sprite:
    一对一的检测
    collide_rect(left, right) -> bool:
        left和right都是Sprite，利用Sprite.rect进行碰撞检测
    collide_rect_ratio(ratio) -> collided_callable:
        上一个函数的扩展，这个函数需要一个额外的浮点类型的参数。这个参数用来指定检测矩形的百分比。
        这是因为，有的时候我们希望冲突检测更精准一些的话，就可以收缩检测的区域，让矩形更小一些，就是通过这个参数控制的。
        注意到该函数会返回一个新的callable对象，使用方法如下:
        >> result = pygame.sprite.collide_rect_ratio( 0.5 )(sprite_1,sprite_2)
    collide_circle(left, right) -> bool:
        使用圆形检测方法
        Sprite必须有rect属性，如果Sprite有radius属性就使用该属性来构造检测圆域
        否则就由程序自行计算
    collide_circle_ratio(ratio) -> collided_callable:
        同理
    collide_mask(SpriteLeft, SpriteRight) -> point:
        返回掩码冲突时掩码上的第一个点，如果没有冲突则返回None。
        Sprite必须有rect属性，最好有mask属性，mask属性的构造方法如下:
        >> sprite.mask = pygame.mask.from_surface(sprite.image)

    一对多的检测
    spritecollide(sprite, group, dokill, collided = None) -> Sprite_list:
        返回一个列表，其中包含与另一个精灵相交的组中的所有精灵。
        相交是通过比较 Sprite.rect来确定的
        dokill参数是一个bool。如果设置为True，所有碰撞的精灵都将从组中移除。
        collided是一个回调函数，用于计算两个精灵是否冲突。它应该将两个sprites作为值，并返回一个bool值，该值指示它们是否发生冲突，比如pygame.sprite.collide_rect等等
        如果没有collided参数，所有的精灵都必须有一个“rect”属性
    spritecollideany(sprite, group, collided = None) -> None|Sprite:
        如果相撞，返回单个Sprite，这是上一个函数的简化版，运行速度更快

    多对多的检测:
    groupcollide(group1, group2, dokill1, dokill2, collided = None) -> Sprite_dict
"""
import sys

import pygame
import pygame.draw as draw
import pygame.transform as transform
from pygame.rect import Rect
from pygame.surface import Surface
from vector import Vector
import random
import tkinter
import tkinter.messagebox


class Ball(pygame.sprite.Sprite):
    def __init__(self, screenSize, loc, speed=200):
        super().__init__()
        self.image = pygame.image.load(r'./Image/ball.png').convert_alpha()
        self.image = transform.scale(self.image, (20, 20))
        self.rect = Rect(
            loc[0], loc[1],
            self.image.get_width(), self.image.get_height()
        )
        vx = random.randint(10, 100)
        vy = random.randint(10, 100)
        # 方向向量
        self.direction = Vector((vx, vy)).normalize()
        self.xlim = screenSize[0]
        self.ylim = screenSize[1]
        self.speed = speed

    def update(self, dt):
        if self.rect.bottom >= self.ylim:
            return False
        if self.rect.top <= 0:
            # 防止球已经超过边界，造成反复reverse的情况
            beyond = -self.rect.top
            if beyond > 0:
                self.move('down', beyond)
            self.reverseY()
        if self.rect.left <= 0:
            beyond = -self.rect.left
            if beyond > 0:
                self.move('right', beyond)
            self.reverseX()
        if self.rect.right >= self.xlim:
            beyond = self.rect.right - self.xlim
            if beyond > 0:
                self.move('left', beyond)
            self.reverseX()
        shift = self.direction * self.speed * dt
        self.rect = self.rect.move(shift.x, shift.y)
        return True

    def reverseX(self):
        self.direction.x = -self.direction.x

    def move(self, direction='up', by=0):
        """往某方向移动多少距离"""
        if direction == 'up':
            self.rect = self.rect.move(0, -by)
        elif direction == 'down':
            self.rect = self.rect.move(0, by)
        elif direction == 'left':
            self.rect = self.rect.move(-by, 0)
        elif direction == 'right':
            self.rect = self.rect.move(by, 0)

    def reverseY(self):
        self.direction.y = -self.direction.y

    def baffleCollisionDetect(self, baffle):
        point = pygame.sprite.collide_mask(self, baffle)
        if point:
            beyond = self.rect.bottom - baffle.rect.top
            if beyond > 0:
                self.move('up', beyond)
            self.reverseY()
            # print(point)

    def obstacleCollisionDetect(self, group):
        res = pygame.sprite.spritecollide(self, group, True)
        if res != []:
            print('Collision with', res)
            self.reverseY()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.image = Surface((rect[2], rect[3]))
        self.image.fill((100, 100, 100))
        self.rect = Rect(*rect)
        draw.rect(self.image, (0, 0, 0),
                  (0, 0, rect[2], rect[3]), 1)

    def update(self):
        pass


class Baffle(pygame.sprite.Sprite):
    def __init__(self, screecSize):
        super().__init__()
        self.xlim = screecSize[0]
        self.ylim = screecSize[1]
        self.image = pygame.image.load(r'./Image/Baffle.png').convert_alpha()
        self.image = transform.scale(self.image, (100, 15))
        self.rect = Rect(self.xlim // 2 - 50, self.ylim - 15 - 5,
                         100, 15)
        self.speed = 200

    def update(self, dt):
        keys = pygame.key.get_pressed()
        dx = dt * self.speed
        if keys[pygame.K_RIGHT]:
            self.moveRight(dx)
        if keys[pygame.K_LEFT]:
            self.moveLeft(dx)

    def moveRight(self, dx):
        toRight = self.xlim - self.rect.right
        if toRight <= 0:
            return
        elif toRight < dx:
            self.rect = self.rect.move(toRight, 0)
        else:
            self.rect = self.rect.move(dx, 0)

    def moveLeft(self, dx):
        toLeft = self.rect.left
        if toLeft <= 0:
            return
        elif toLeft < dx:
            self.rect = self.rect.move(-toLeft, 0)
        else:
            self.rect = self.rect.move(-dx, 0)


class Game(object):
    def __init__(self, screenSize, FPS=40):
        pygame.init()
        self.size = screenSize
        self.screen = pygame.display.set_mode(screenSize)
        pygame.display.set_caption('Collision Test')
        self.initWidgets()
        pygame.event.set_blocked([
            pygame.MOUSEMOTION
        ])
        self.FPS = FPS
        self.clock = pygame.time.Clock()

    def initWidgets(self):
        self.ball = Ball(self.size, (180, 320))
        self.baffle = Baffle(self.size)
        # 按照一定概率随机分布
        rate = 0.3
        row, col = 25, 10
        width = self.size[0] // col
        height = 10
        self.obstacleGroup = pygame.sprite.Group()
        startAt = 50
        for r in range(row):
            for c in range(col):
                rect = (c * width, startAt + height * r, width, height)
                v = random.randint(1, 100) / 100
                if v <= rate:
                    obs = Obstacle(rect)
                    self.obstacleGroup.add(obs)

    def run(self):
        while True:
            self.dt = self.clock.tick(self.FPS) / 1000
            self.event()
            self.update(self.dt)
            self.draw()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()

    def update(self, dt):
        self.ball.baffleCollisionDetect(self.baffle)
        self.ball.obstacleCollisionDetect(self.obstacleGroup)
        res = self.ball.update(dt)
        self.baffle.update(dt)
        if not res:
            # 隐藏主界面
            tkinter.Tk().wm_withdraw()
            tkinter.messagebox.showerror('Failed', '你输了!')
            self.exit()

    def exit(self):
        pygame.quit()
        sys.exit()

    def draw(self):
        self.screen.fill((80, 115, 130))
        self.screen.blit(self.ball.image, self.ball.rect)
        self.screen.blit(self.baffle.image, self.baffle.rect)
        self.obstacleGroup.draw(self.screen)
        pygame.display.update()


if __name__ == '__main__':
    game = Game(screenSize=(360, 480))
    game.run()
