import colorama


class PowerUp:

    power_up_symbols = (
        colorama.Fore.YELLOW+"="+colorama.Fore.RESET,
        colorama.Fore.RED+"="+colorama.Fore.RESET,
        colorama.Fore.YELLOW+"O"+colorama.Fore.RESET,
        colorama.Fore.RED+"O"+colorama.Fore.RESET,
        colorama.Fore.GREEN+"O"+colorama.Fore.RESET,
        colorama.Fore.GREEN+"="+colorama.Fore.RESET
    )

    def __init__(self, r, c, symbol):
        self.r = r
        self.c = c
        self.time_left = 12
        self.symbol = symbol
        self.active = False

    def set_active(self, state):
        self.active = state

    def update_position(self, grid, paddle, catchable_power_ups, active_power_ups):
        grid[self.r][self.c] = " "
        self.r += 1
        position = paddle.get_position()
        if self.r == position[0] and position[1] <= self.c < position[1] + paddle.length:
            catchable_power_ups.remove(self)
            active_power_ups.append(self)
        if grid[self.r][self.c] == " ":
            grid[self.r][self.c] = self.symbol

    def decrease_timer(self, sleep_time):
        self.time_left -= sleep_time


class ExpandPaddle(PowerUp):
    def __init__(self, r, c):
        super().__init__(r, c, PowerUp.power_up_symbols[0])

    def activate(self, paddle, grid):
        self.active = True
        paddle.increase_length(2)

    def deactivate(self, paddle, grid):
        self.active = False
        paddle.decrease_length(2, grid)


class ShrinkPaddle(PowerUp):
    def __init__(self, r, c):
        super().__init__(r, c, PowerUp.power_up_symbols[1])

    def activate(self, paddle, grid):
        self.active = True
        paddle.decrease_length(2, grid)

    def deactivate(self, paddle, grid):
        self.active = False
        paddle.increase_length(2)


class FastBall(PowerUp):
    def __init__(self, r, c):
        super().__init__(r, c, PowerUp.power_up_symbols[3])

    def activate(self, balls, grid):
        self.active = True
        for ball in balls:
            ball.multiply_speed(2)

    def deactivate(self, balls, grid):
        self.active = True
        for ball in balls:
            ball.multiply_speed(1/2)


class ThroughBallPowerUp(PowerUp):
    def __init__(self, r, c):
        super().__init__(r, c, PowerUp.power_up_symbols[4])
