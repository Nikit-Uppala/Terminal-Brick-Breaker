from ball import Ball
import colorama
from time import sleep

class Brick:

    brick_length = 6
    colors = [None, colorama.Fore.GREEN, colorama.Fore.BLUE, colorama.Fore.RED, ""]
    color_reset = colorama.Fore.RESET
    brick_structure = [[x for x in "------"], ["|", " ", " ", " ", " ", "|"], [x for x in "------"]]

    def __init__(self, health, r, c, score):
        self.health = health
        self.r = r
        self.c = c
        self.score = score

    def remove_from_grid(self, grid):
        for r in range(-1, 2):
            for c in range(Brick.brick_length):
                grid[self.r+r][self.c+c] = " "

    def update_score(self):
        return self.score

    def on_hit(self):
        if self.health > 0:
            self.health -= 1

    def display_on_grid(self, grid, balls):
        for r in range(-1, 2):
            for c in range(Brick.brick_length):
                if (r == -1 or r == 1) and grid[self.r+r][self.c+c] == Ball.symbol:
                    for ball in balls:
                        position = ball.get_position()
                        velocity = ball.get_velocity()
                        if position[0] == self.r+r and position[1] == self.c+c:
                            if (r == -1 and velocity[0] < 0) or (r == 1 and velocity[0] > 0):
                                if velocity[1] > 0:
                                    ball.set_position(self.r, self.c)
                                else:
                                    ball.set_position(self.r, self.c+Brick.brick_length-1)
                                ball.collision_with_brick_horizontal()
                            else:
                                ball.collision_with_brick_vertical()
                    self.on_hit()
                elif r == 0 and (c == 0 or c == Brick.brick_length-1) and grid[self.r][self.c+c] == Ball.symbol:
                    for ball in balls:
                        position = ball.get_position()
                        if position[0] == self.r+r and position[1] == self.c+c:
                            ball.collision_with_brick_horizontal()
                    self.on_hit()
                else:
                    grid[self.r+r][self.c+c] = Brick.brick_structure[r+1][c]
        if self.health != 0:
            for r in range(-1, 2):
                grid[self.r+r][self.c] = Brick.colors[self.health]+grid[self.r+r][self.c]
                col = self.c+Brick.brick_length-1
                grid[self.r+r][col] = grid[self.r+r][col]+Brick.color_reset


class NonBreakableBrick(Brick):

    def __init__(self, r, c):
        super().__init__(-1, r, c, 100)

    def on_hit(self):
        pass
