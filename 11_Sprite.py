"""
使用精灵，以更加OOP的方法组织各种图片动画
要点:
使用Sprite
1. 创建一个类继承Sprite
2. 新的子类要有image和rect两个属性
3. 新的子类中重写update方法, 在update方法中编写Sprite发生变化的代码
   可以把update的任务看作是指明从某一帧到下一帧发生了什么变化

以下部分可选，不想使用Group的话也无所谓，而且自由度还会高一些

4. 创建Group对象
5. 将所有精灵对象加入group
6. 调用group.update, 它会自动调用所有精灵的update方法
7. 调用group.draw, 它会将所有精灵blit到某个Surface上(参数指定)
   在每个Sprite中, image制定了blit的内容, rect指定了blit的位置, 比如:screen.blit(b.image, b.rect)

pygame.sprite:
    Sprite(*groups) -> Sprite:
        update(*args) -> None
    Group(*sprites) -> Group:
        sprites() -> sprite_list
        add(*sprites) -> None
        remove(*sprites) -> None
        update(*args) -> None:
            自动调用所有Group中的Sprite
            传给update的参数会被传给每一个Sprite的update
        draw(Surface) -> None:
            将每个sprite绘制到Surface上面
"""

import pygame
from pygame import sprite

SIZE = WIDTH, HEIGHT = 600, 400
BACKGROUND_COLOR = pygame.Color('white')
FPS = 10


class MySprite(sprite.Sprite):
    def __init__(self, parent):
        super(MySprite, self).__init__()
        self.parent = parent
        self.images = []
        self.images.append(pygame.image.load('Image/walk1.png'))
        self.images.append(pygame.image.load('Image/walk2.png'))
        self.images.append(pygame.image.load('Image/walk3.png'))
        self.images.append(pygame.image.load('Image/walk4.png'))
        self.images.append(pygame.image.load('Image/walk5.png'))
        self.images.append(pygame.image.load('Image/walk6.png'))
        self.images.append(pygame.image.load('Image/walk7.png'))
        self.images.append(pygame.image.load('Image/walk8.png'))
        self.images.append(pygame.image.load('Image/walk9.png'))
        self.images.append(pygame.image.load('Image/walk10.png'))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(50, 50, 150, 198)

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        pygame.draw.rect(self.parent, (100, 100, 100), self.rect, 5)


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    mySprite = MySprite(screen)
    group = sprite.Group(mySprite)
    clock = pygame.time.Clock()
    while True:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(BACKGROUND_COLOR)
        group.update()
        group.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
