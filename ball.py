import random
from powerup import PowerUp


class Ball:

    symbol = "O"

    def __init__(self, r, c, v_r, v_c, paddle_length, grid, held):
        self.r = r
        self.c = c if paddle_length == 0 else random.randint(c+1, c+paddle_length-2)
        self.v_r = v_r
        self.v_c = v_c
        self.temp_v_r = -1 if paddle_length != 0 else 0
        self.position_held = -1 if paddle_length == 0 else self.c - c
        self.temp_v_c = -(paddle_length // 2) + self.position_held if paddle_length != 0 else 0
        self.held = held
        grid[self.r][self.c] = Ball.symbol

    def get_position(self):
        return self.r, self.c

    def get_velocity(self):
        return self.v_r, self.v_c

    def set_position(self, r, c, grid):
        self.r = r
        self.c = c
        grid[self.r][self.c] = Ball.symbol

    def collision_with_vertical_wall(self):
        self.v_r = -self.v_r

    def collision_with_horizontal_wall(self):
        self.v_c = -self.v_c

    def collision_with_paddle(self, col, length):
        end_deviation = -(length//2)
        result_deviation = end_deviation + col
        self.v_c += result_deviation
        self.v_r = -self.v_r

    def collision_with_brick_vertical(self):
        self.v_r = -self.v_r

    def collision_with_brick_horizontal(self):
        self.v_c = -self.v_c

    def stop(self, col, length):
        self.temp_v_r = -self.v_r
        self.temp_v_c = self.v_c - (length//2) + col
        self.position_held = col
        self.v_r = 0
        self.v_c = 0
        self.held = True

    def move_with_paddle(self, grid, paddle_c):
        self.c = paddle_c + self.position_held
        grid[self.r][self.c] = Ball.symbol

    def release(self, grid):
        self.held = False
        self.position_held = -1
        self.v_r = self.temp_v_r
        self.v_c = self.temp_v_c
        self.update_position(grid)

    def _set_new_position(self, grid):
        if self.v_c == 0:
            for r in range(1, self.v_r+1):
                if grid[self.r+r][self.c] != " " and grid[self.r+r][self.c] != Ball.symbol and \
                        not(grid[self.r+r][self.c] in PowerUp.power_up_symbols):
                    return self.r+r, self.c
        elif self.v_c >= self.v_r:
            ratio = self.v_c // self.v_r
            for r in range(1, self.v_r+1):
                for c in range(1, ratio+1):
                    row, col = self.r+r, self.c+c+(r-1)*ratio
                    if grid[row][col] != " " and grid[row][col] != Ball.symbol and \
                            not(grid[row][col] in PowerUp.power_up_symbols):
                        return row, col
        else:
            ratio = self.v_r // self.v_c
            for c in range(1, self.v_c+1):
                for r in range(1, ratio+1):
                    row, col = self.r+r+(c-1)*ratio, self.c+c
                    if grid[row][col] != " " and grid[row][col] != Ball.symbol and \
                            not(grid[row][col] in PowerUp.power_up_symbols):
                        return row, col
        return self.r+self.v_r, self.c+self.v_c

    def update_position(self, grid):
        if self.v_c == 0 and self.v_r == 0:
            grid[self.r][self.c] = Ball.symbol
            return
        new_r, new_c = self._set_new_position(grid)
        if new_r >= len(grid)-1:
            new_r = len(grid)-1
        elif new_r <= 0:
            self.collision_with_vertical_wall()
            new_r = 0
        if new_c <= 0 or new_c >= len(grid[0]) - 1:
            self.collision_with_horizontal_wall()
            new_c = 0 if new_c <= 0 else len(grid[0]) - 1
        grid[self.r][self.c] = " "
        if self.c <= 0 or self.c >= len(grid[0])-1:
            grid[self.r][self.c] = "|"
        if self.r <= 0:
            grid[self.r][self.c] = "-"
        self.set_position(new_r, new_c, grid)
