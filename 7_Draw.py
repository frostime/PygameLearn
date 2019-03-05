"""
绘制图形
pygame.draw:
    返回值都是一个Rect对象，包含了绘制的领域，这样你就可以很方便的更新那个部分了
    rect(Surface, color, Rect, width=0) -> Rect
        width 是指线宽, 如果线宽是0或省略, 表示填充(fill)
    polygon(Surface, color, pointlist, width=0) -> Rect
        绘制多边形
    circle(Surface, color, pos, radius, width=0) -> Rect
    ellipse(Surface, color, Rect, width=0) -> Rect
        绘制椭圆, Rect是椭圆外接矩形
    arc(Surface, color, Rect, start_angle, stop_angle, width=1) -> Rect
        绘制弧, 官方的解释是椭圆的局部
        Rect就是椭圆的外接矩形
        start_angle和stop_angle是指起始角度, 按极坐标的标注来, 以x轴正方向为0度
    line(Surface, color, start_pos, end_pos, width=1) -> Rect
    lines(Surface, color, closed, pointlist, width=1) -> Rect
        画线
    aaline(Surface, color, startpos, endpos, blend=1) -> Rect
    aalines(Surface, color, closed, pointlist, blend=1) -> Rect
        同上, aa表示抗锯齿
"""
import pygame
from math import pi

# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
BLUE = (0,   0, 255)
GREEN = (0, 255,   0)
RED = (255,   0,   0)

# Set the height and width of the screen
size = [400, 300]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Example code for the draw module")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

while not done:

    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(10)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    # All drawing code happens after the for loop and but
    # inside the main while done==False loop.

    # Clear the screen and set the screen background
    screen.fill(WHITE)

    # Draw on the screen a GREEN line from (0,0) to (50.75)
    # 5 pixels wide.
    pygame.draw.line(screen, GREEN, [0, 0], [50, 30], 5)

    # Draw on the screen a GREEN line from (0,0) to (50.75)
    # 5 pixels wide.
    pygame.draw.lines(screen, BLACK, False, [
                      [0, 80], [50, 90], [200, 80], [220, 30]], 5)

    # Draw on the screen a GREEN line from (0,0) to (50.75)
    # 5 pixels wide.
    pygame.draw.aaline(screen, GREEN, [0, 50], [50, 80], True)

    # Draw a rectangle outline
    pygame.draw.rect(screen, BLACK, [75, 10, 50, 20], 2)

    # Draw a solid rectangle
    pygame.draw.rect(screen, BLACK, [150, 10, 50, 20])

    # Draw an ellipse outline, using a rectangle as the outside boundaries
    pygame.draw.ellipse(screen, RED, [225, 10, 50, 20], 2)

    # Draw an solid ellipse, using a rectangle as the outside boundaries
    pygame.draw.ellipse(screen, RED, [300, 10, 50, 20])

    # This draws a triangle using the polygon command
    pygame.draw.polygon(screen, BLACK, [[100, 100], [0, 200], [200, 200]], 5)

    # Draw an arc as part of an ellipse.
    # Use radians to determine what angle to draw.
    pygame.draw.arc(screen, BLACK, [210, 75, 150, 125], 0, pi/2, 2)
    pygame.draw.arc(screen, GREEN, [210, 75, 150, 125], pi/2, pi, 2)
    pygame.draw.arc(screen, BLUE, [210, 75, 150, 125], pi, 3*pi/2, 2)
    pygame.draw.arc(screen, RED,  [210, 75, 150, 125], 3*pi/2, 2*pi, 2)

    # Draw a circle
    pygame.draw.circle(screen, BLUE, [60, 250], 40)

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()

# Be IDLE friendly
pygame.quit()
