from input import input_to, Get
from ball import Ball
import colorama
from time import sleep


class Paddle:

    symbol = "="

    def collision_with_ball(self, balls, i, grid):
        for ball in balls:
            if ball.r == self.r and ball.c == self.c + i:
                if not ball.held:
                    ball.collision_with_paddle(i, self.length)
                else:
                    grid[self.r][self.c + i] = Paddle.symbol
                    ball.move_with_paddle(grid, self.c)

    def display_in_grid(self, grid, balls):
        for i in range(self.length):
            if grid[self.r][self.c+i] == Ball.symbol:
                self.collision_with_ball(balls, i, grid)
            else:
                grid[self.r][self.c+i] = Paddle.symbol

    def increase_length(self, increase):
        self.length = self.length + increase

    def decrease_length(self, decrease, grid):
        self.length = self.length - decrease
        end_col = self.c + self.length-1
        for i in range(decrease):
            grid[self.r][end_col+i+1] = " "

    def __init__(self, length, r, c):
        self.length = length
        self.r = r
        self.c = c
        self.step_size = 1

    def get_position(self):
        return self.r, self.c

    def _move_left(self, grid):
        old_end = self.c+self.length - 1
        self.c -= self.step_size
        self.c = 1 if self.c <= 1 else self.c
        if self.c+self.length-1 != old_end:
            for i in range(self.step_size):
                grid[self.r][old_end-i] = " "

    def _move_right(self, grid):
        old_start = self.c
        self.c += self.step_size
        self.c = len(grid[0])-1-self.length if self.c+self.length >= len(grid[0])-2 else self.c
        if self.c != old_start:
            for i in range(self.step_size):
                grid[self.r][old_start+i] = " "

    def move_paddle(self, grid, balls, catch_power_ups, active_power_ups, timeout):
        get_key = Get()
        direction = input_to(get_key, timeout)
        if direction is not None:
            if direction == "a":
                self._move_left(grid)
            elif direction == "d":
                self._move_right(grid)
            elif ord(direction) == 32:
                for ball in balls:
                    if ball.held:
                        ball.release(grid)
                        break
        self.display_in_grid(grid, balls)


class GrabPaddle(Paddle):

    def __init__(self, length, r, c):
        super().__init__(length, r, c)

    def collision_with_ball(self, balls, i, grid):
        for ball in balls:
            if ball.r == self.r and ball.c == self.c + i:
                if not ball.held:
                    ball.stop(i, self.length)
                else:
                    grid[self.r][self.c + i] = Paddle.symbol
                    ball.move_with_paddle(grid, self.c)
