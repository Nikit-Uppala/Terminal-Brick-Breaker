from brick import Brick, NonBreakableBrick
import random as rnd


def generate_bricks(resolution):
    bricks = []
    rows = resolution[0]
    cols = resolution[1]
    start_row, end_row = 3, 9
    start_col, end_col = 4, cols-12
    for r in range(start_row, end_row+1, 3):
        for c in range(start_col, end_col, Brick.brick_length+2):
            if r == start_row or r == end_row:
                health = rnd.randint(1, 3)
                bricks.append(Brick(health, r, c, health*20-10))
            else:
                type_brick = rnd.random()
                if type_brick > 0.5:
                    bricks.append(NonBreakableBrick(r, c))
                else:
                    health = rnd.randint(1, 3)
                    bricks.append(Brick(health, r, c, 20*health-10))
    return bricks
