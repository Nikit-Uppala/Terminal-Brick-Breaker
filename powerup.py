import colorama
# from ball import Ball
# from paddle import Paddle


class PowerUp:

    power_up_symbols = (
        # colorama.Fore.YELLOW+Paddle.symbol+colorama.Fore.RESET,
        # colorama.Fore.RED+Paddle.symbol+colorama.Fore.RESET,
        # colorama.Fore.YELLOW+Ball.symbol+colorama.Fore.RESET,
        # colorama.Fore.RED+Ball.symbol+colorama.Fore.RESET,
        # colorama.Fore.GREEN+Ball.symbol+colorama.Fore.RESET,
        # colorama.Fore.GREEN+Paddle.symbol+colorama.Fore.RESET
    )

    @staticmethod
    def activate():
        pass

    def __init__(self, r, c, catchable_list, grid, symbol):
        self.r = r
        self.c = c
        self.time_left = 5
        self.symbol = symbol
        catchable_list.append(self)

    def update_position(self, grid, paddle, balls, catchable_power_ups, active_power_ups):
        grid[self.r][self.c] = " "
        self.r += 1
        if self.r == paddle.r and paddle.c <= self.c < paddle.c + paddle.length:
            catchable_power_ups.remove(self)
            if "=" in self.symbol:
                self.activate(paddle, grid)
            else:
                self.activate(balls, grid)
            active_power_ups.append(self)
        grid[self.r][self.c] = self.symbol

    def decrease_timer(self, sleep_time):
        self.time_left -= 2*sleep_time


class ExpandPaddle(PowerUp):
    def __init__(self, r, c, catchable_list, grid):
        super().__init__(r, c, catchable_list, grid, PowerUp.power_up_symbols[0])

    @staticmethod
    def activate(paddle, grid):
        paddle.increase_length(2)

    @staticmethod
    def deactivate(paddle, grid):
        paddle.decrease_length(2, grid)


class ShrinkPaddle(PowerUp):
    def __init__(self, r, c, catchable_list, grid):
        super().__init__(r, c, catchable_list, grid, PowerUp.power_up_symbols[1])

    @staticmethod
    def activate(paddle, grid):
        paddle.decrease_length(2, grid)

    @staticmethod
    def deactivate(paddle, grid):
        paddle.increase_length(2)


# class BallMultiplier(PowerUp):
#     def __init__(self, r, c, catchable_list, grid):
#         super().__init__(r, c, catchable_list, grid, PowerUp.power_up_symbols[2])
#
#     @staticmethod
#     def activate(balls, grid):
#         new_balls = []
#         for ball in balls:
#             new_balls.append(Ball(ball.r, ball.c, ball.v_r, -ball.v_c, 0, grid, ball.held))
#
#     @staticmethod
#     def deactivate(balls, grid):
#         if len(balls) >= 2:
#             temp_ball = balls[-1]
#             balls.pop()
#             grid[temp_ball.r][temp_ball.c] = " "
#             del temp_ball


class FastBall(PowerUp):
    def __init__(self, r, c, catchable_list, grid):
        super().__init__(r, c, catchable_list, grid, PowerUp.power_up_symbols[3])

    @staticmethod
    def activate(balls, grid):
        for ball in balls:
            ball.multiply_speed(2)

    @staticmethod
    def deactivate(balls, grid):
        for ball in balls:
            ball.multiply_speed(1/2)
