from board import Board
from ball import Ball
from paddle import Paddle, GrabPaddle
from brick import Brick, NonBreakableBrick
from os import get_terminal_size
import random as rnd
from powerup import ExpandPaddle, ShrinkPaddle, FastBall, PowerUp
import colorama
from time import sleep


def handle_balls():
    global Balls, started, lives, game_over, grid, paddle
    for ball in Balls:
        position = ball.get_position()
        if position[0] == len(grid)-1:
            grid[position[0]][position[1]] = "-"
            Balls.remove(ball)
            del ball
        elif not ball.held:
            started = True
            ball.update_position(grid)
    if len(Balls) == 0:
        lives -= 1
        if lives > 0:
            Balls.append(Ball(paddle.r, paddle.c, 0, 0, paddle.length, grid, True))
        else:
            game_over = True


def generate_power_up(brick):
    global power_up_probability, catchable_power_ups, num_power_ups
    random_number = rnd.random()
    if random_number <= power_up_probability:
        type_power_up = rnd.randint(0, num_power_ups-1)
        if type_power_up == 0:
            catchable_power_ups.append(ExpandPaddle(brick.r, brick.c+Brick.brick_length//2))
        elif type_power_up == 1:
            catchable_power_ups.append(ShrinkPaddle(brick.r, brick.c+Brick.brick_length//2))
        elif type_power_up == 2:
            catchable_power_ups.append(
                PowerUp(brick.r, brick.c+Brick.brick_length//2, PowerUp.power_up_symbols[type_power_up]))
        elif type_power_up == 3:
            catchable_power_ups.append(FastBall(brick.r, brick.c+Brick.brick_length//2))
        elif type_power_up == 4:
            catchable_power_ups.append(
                PowerUp(brick.r, brick.c+Brick.brick_length//2, PowerUp.power_up_symbols[type_power_up]))
        elif type_power_up == 5:
            catchable_power_ups.append(
                PowerUp(brick.r, brick.c+Brick.brick_length//2, PowerUp.power_up_symbols[type_power_up]))


def handle_bricks():
    global Bricks, score
    for brick in Bricks:
        if brick.health == 0:
            brick.remove_from_grid(grid)
            Bricks.remove(brick)
            score += brick.update_score()
            generate_power_up(brick)
            del brick
        else:
            brick.display_on_grid(grid, Balls)


def handle_ball_multiplier():
    global Balls
    new_balls = []
    for ball in Balls:
        new_balls.append(Ball(ball.r, ball.c, ball.v_r, ball.v_c+1, 0, grid, False))
    for new_ball in new_balls:
        Balls.append(new_ball)


def handle_power_ups():
    global catchable_power_ups, active_power_ups, grid, Balls, paddle
    for power_up in catchable_power_ups:
        if power_up.r == len(grid)-1:
            catchable_power_ups.remove(power_up)
            grid[power_up.r][power_up.c] = "-"
            del power_up
        else:
            power_up.update_position(grid, paddle, catchable_power_ups, active_power_ups)
    for power_up in active_power_ups:
        if power_up.active:
            power_up.decrease_timer(time_gap)
        else:
            if "=" in power_up.symbol:
                if colorama.Fore.GREEN in power_up.symbol:
                    paddle = GrabPaddle(paddle.length, paddle.r, paddle.c)
                    power_up.set_active(True)
                else:
                    power_up.activate(paddle, grid)
            else:
                if colorama.Fore.GREEN in power_up.symbol:
                    pass
                elif colorama.Fore.YELLOW in power_up.symbol:
                    handle_ball_multiplier()
                    power_up.set_active(True)
                else:
                    power_up.activate(Balls, grid)
        if power_up.time_left <= 0:
            if "=" in power_up.symbol:
                if colorama.Fore.GREEN in power_up.symbol:
                    paddle = Paddle(paddle.length, paddle.r, paddle.c)
                    power_up.set_active(False)
                else:
                    power_up.deactivate(paddle, grid)
            else:
                if colorama.Fore.GREEN in power_up.symbol:
                    pass
                elif colorama.Fore.YELLOW in power_up.symbol:
                    if len(Balls) > 1:
                        Balls.pop()
                    power_up.set_active(False)
                else:
                    power_up.deactivate(Balls)
            active_power_ups.remove(power_up)
            del power_up


power_up_probability = 0.4
num_power_ups = 6
terminal_size = get_terminal_size(0)
resolution = (terminal_size.lines-3, terminal_size.columns-2)
grid = []
board = Board(resolution[0], resolution[1], grid)
board.create_grid()
Balls = []
Bricks = [Brick(2, 2, 15, 30), Brick(1, 10, 10, 10)]
paddle = Paddle(7, resolution[0]-2, resolution[1]//2)
Balls.append(Ball(paddle.r, paddle.c, 0, 0, paddle.length, grid, True))
lives = 3
score = 0
time = 0
catchable_power_ups = []
active_power_ups = []
game_over = False
time_gap = 0.1
started = False

while not game_over:
    direction = Board.display_game_details(lives, score, time, time_gap)
    board.print_grid()
    if len(Bricks) == 0:
        game_over = True
    if started:
        time += time_gap
    handle_power_ups()
    handle_balls()
    paddle.move_paddle(grid, Balls, direction)
    handle_bricks()
if len(Bricks) == 0:
    print("\t\t\t\t\tYou Won")
else:
    print("\t\t\t\t\tGame Over")
