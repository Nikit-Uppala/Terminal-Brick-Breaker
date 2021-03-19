import colorama
from time import sleep

class PowerUp:

    power_up_symbols = (
        colorama.Fore.YELLOW+"="+colorama.Fore.RESET,
        colorama.Fore.RED+"="+colorama.Fore.RESET,
        colorama.Fore.YELLOW+"O"+colorama.Fore.RESET,
        colorama.Fore.RED+"O"+colorama.Fore.RESET,
        colorama.Fore.GREEN+"O"+colorama.Fore.RESET,
        colorama.Fore.GREEN+"="+colorama.Fore.RESET,
        colorama.Fore.YELLOW+"^"+colorama.Fore.RESET
    )

    def __init__(self, r, c, symbol, velocity):
        self.r = r
        self.c = c
        self.time_left = 6
        self.symbol = symbol
        self.active = False
        self.v_r = velocity[0]
        self.v_c = velocity[1]
        self.a_c = 1
        self.frames = 0

    def set_active(self, state):
        self.active = state
    
    def collision_with_horizontal_wall(self):
        self.v_r = -self.v_r
    
    def collision_with_vertical_wall(self):
        self.v_c = -self.v_c
    
    def _get_new_position(self, grid, paddle):
        if self.v_c == 0 and self.v_r == 0:
            return self.r, self.c
        elif self.v_c == 0:
            for r in range(1, self.v_r+1):
                if self.r+r == paddle.r and paddle.c <= self.c < paddle.c+paddle.length:
                    return self.r+r, self.c
        elif self.v_r == 0:
            for c in range(1, self.v_c+1):
                if self.c+c == 0 or self.c+c == len(grid[0])-1:
                    return self.r, self.c+c
        else:
            if self.v_c >= self.v_r:
                ratio = self.v_c // self.v_r
                for r in range(1, self.v_r+1):
                    row = self.r+r
                    for c in range(1, ratio+1):
                        col = self.c+c+(r-1)*ratio
                        if row == 0:
                            return row, col
                        elif col == 0 or col == len(grid[0]) - 1:
                            return row, col
                        elif row == paddle.r and paddle.c <= col < paddle.c+paddle.length:
                            return row, col
            else:
                ratio = self.v_r // self.v_c
                for c in range(1, self.v_c+1):
                    col = self.c+c
                    for r in range(1, ratio+1):
                        row = self.r+r+(c-1)*ratio
                        if row == 0:
                            return row, col
                        elif col == 0 or col == len(grid[0]) - 1:
                            return row, col
                        elif row == paddle.r and paddle.c <= col < paddle.c+paddle.length:
                            return row, col
        return self.r+self.v_r, self.c+self.v_c

    def update_position(self, grid, paddle, catchable_power_ups, active_power_ups):
        new_r, new_c = self._get_new_position(grid, paddle)
        print(self.r, self.c, new_r, new_c)
        if new_r <= 0:
            new_r = 0
            self.collision_with_horizontal_wall()
        if new_c <=0 or new_c >= len(grid[0])-1:
            new_c = 0 if new_c == 0 else len(grid[0])
            self.collision_with_vertical_wall()
        if new_r == paddle.r and paddle.c <= new_c < paddle.c+paddle.length:
            catchable_power_ups.remove(self)
            active_power_ups.append(self)
        if grid[new_r][new_c] == " ":
            grid[new_r][new_c] = self.symbol
        if grid[self.r][self.c] == self.symbol:
            grid[self.r][self.c] = " "
        self.r, self.c = new_r, new_c
        self.frames += 1
        if self.frames > 2:
            self.frames = 0
            if self.v_r < 2:
                self.v_r += self.a_c

    def remove_from_grid(self, grid):
        if grid[self.r][self.c] == self.symbol:
            grid[self.r][self.c] = " "

    def decrease_timer(self, sleep_time):
        self.time_left -= sleep_time


class ExpandPaddle(PowerUp):
    def __init__(self, r, c, velocity):
        super().__init__(r, c, PowerUp.power_up_symbols[0], velocity)

    def activate(self, paddle, grid):
        self.active = True
        paddle.increase_length(2)

    def deactivate(self, paddle, grid):
        self.active = False
        paddle.decrease_length(2, grid)


class ShrinkPaddle(PowerUp):
    def __init__(self, r, c, velocity):
        super().__init__(r, c, PowerUp.power_up_symbols[1], velocity)

    def activate(self, paddle, grid):
        self.active = True
        paddle.decrease_length(2, grid)

    def deactivate(self, paddle, grid):
        self.active = False
        paddle.increase_length(2)


class FastBall(PowerUp):
    def __init__(self, r, c, velocity):
        super().__init__(r, c, PowerUp.power_up_symbols[3], velocity)

    def activate(self, balls, grid):
        self.active = True
        for ball in balls:
            ball.multiply_speed(2)

    def deactivate(self, balls, grid):
        self.active = True
        for ball in balls:
            ball.multiply_speed(1/2)


class ThroughBallPowerUp(PowerUp):
    def __init__(self, r, c, velocity):
        super().__init__(r, c, PowerUp.power_up_symbols[4], velocity)
