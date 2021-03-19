from brick import Brick, NonBreakableBrick, RainbowBrick
import random as rnd


def generate_bricks(level):
    bricks = []
    if level == 1:
        bricks.append(Brick(1, 4, 16, 10))
        bricks.append(Brick(1, 10, 16, 10))
        bricks.append(RainbowBrick(4, 36))
        bricks.append(Brick(2, 10, 28, 30))
        bricks.append(NonBreakableBrick(10, 60))
    elif level == 2:
        bricks.append(Brick(2, 4, 20, 30))
        bricks.append(NonBreakableBrick(4, 30))
        bricks.append(Brick(2, 4, 55, 30))
        bricks.append(Brick(1, 4, 65, 10))
        bricks.append(RainbowBrick(9, 36))
        bricks.append(Brick(3, 9, 16, 50))
        bricks.append(NonBreakableBrick(9, 60))
        bricks.append(Brick(1, 14, 20, 10))
        bricks.append(Brick(1, 14, 57, 10))
        bricks.append(RainbowBrick(14, 40))
    elif level == 3:
        bricks.append(NonBreakableBrick(6, 8))
        bricks.append(NonBreakableBrick(6, 70))
        bricks.append(NonBreakableBrick(6, 42))




    return bricks
