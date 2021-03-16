from board import Board
from ball import Ball, ThroughBall
from paddle import Paddle, GrabPaddle
from os import get_terminal_size
import random as rnd
from powerup import ExpandPaddle, ShrinkPaddle, FastBall, PowerUp
import colorama
from brick_pattern import generate_bricks
from time import sleep


def activate_power_up(power_up):
    global paddle, grid, Balls
    power_up.set_active(True)
    if "=" in power_up.symbol:
        if colorama.Fore.GREEN in power_up.symbol:
            paddle = GrabPaddle(paddle.length, paddle.r, paddle.c)
        else:
            power_up.activate(paddle, grid)
    else:
        if colorama.Fore.GREEN in power_up.symbol:
            activate_through_ball()
        elif colorama.Fore.YELLOW in power_up.symbol:
            activate_ball_multiplier()
        else:
            power_up.activate(Balls, grid)


def deactivate_power_up(power_up):
    global paddle, grid, Balls
    power_up.set_active(False)
    if "=" in power_up.symbol:
        if colorama.Fore.GREEN in power_up.symbol:
            paddle = Paddle(paddle.length, paddle.r, paddle.c)
        else:
            power_up.deactivate(paddle, grid)
    else:
        if colorama.Fore.GREEN in power_up.symbol:
            deactivate_through_ball()
        elif colorama.Fore.YELLOW in power_up.symbol:
            deactivate_ball_multiplier()
        else:
            power_up.activate(Balls, grid)


def handle_balls():
    global Balls, started, lives, game_over, grid, paddle, life_lost
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
            life_lost = True
            Balls.append(Ball(paddle.r, paddle.c, 0, 0, grid, paddle.length, True))
            for power_up in active_power_ups:
                deactivate_power_up(power_up)
                active_power_ups.remove(power_up)
                del power_up
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
        brick.display_on_grid(grid, Balls)
        if brick.health == 0:
            score += brick.update_score()
            brick.remove_from_grid(grid)
            Bricks.remove(brick)
            del brick


def activate_ball_multiplier():
    global Balls
    new_balls = []
    for ball in Balls:
        if hasattr(ball, "through"):
            new_balls.append(ThroughBall(ball.r, ball.c, -1, -ball.v_c+1, grid))
        else:
            new_balls.append(Ball(ball.r, ball.c, -1, -ball.v_c+1, grid))
    for new_ball in new_balls:
        Balls.append(new_ball)


def deactivate_ball_multiplier():
    global Balls
    num = len(Balls)
    if num > 1:
        to_be_removed = -(-num//2)
        for i in range(to_be_removed):
            grid[Balls[-1].r][Balls[-1].c] = " "
            Balls.pop()


def activate_through_ball():
    global Balls
    new_balls = []
    for ball in Balls:
        new_balls.append(
            ThroughBall(ball.r, ball.c, ball.v_r, ball.v_c, grid,
                        held=ball.held, temp_v_r=ball.temp_v_r, temp_v_c=ball.temp_v_c))
        Balls.remove(ball)
        del ball
    for new_ball in new_balls:
        Balls.append(new_ball)


def deactivate_through_ball():
    global Balls, paddle
    new_balls = []
    for ball in Balls:
        new_balls.append(Ball(ball.r, ball.c, ball.v_r, ball.v_c, grid,
                              held=ball.held, temp_v_c=ball.temp_v_c, temp_v_r=ball.temp_v_r))
        del ball
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
            activate_power_up(power_up)
        if power_up.time_left <= 0:
            deactivate_power_up(power_up)
            active_power_ups.remove(power_up)
            del power_up


def check_game_over():
    global Bricks, level, lives
    for brick in Bricks:
        if brick.health > 0:
            return False
    return True


def reset_objects():
    global Balls, paddle, catchable_power_ups, active_power_ups, Bricks, started, time_limit, level_start_time
    for ball in Balls:
        if 0 < ball.c < resolution[1] or ball.r > 0:
            ball.remove_from_gird(grid)
            Balls.remove(ball)
            del ball
    paddle.remove_from_grid(grid)
    paddle = Paddle(7, resolution[0] - 2, resolution[1] // 2)
    Balls.append(Ball(paddle.r, paddle.c, 0, 0, grid, paddle.length, True))
    for brick in Bricks:
        brick.remove_from_grid(grid)
        Bricks.remove(brick)
        del brick
    Bricks = generate_bricks(resolution, level)
    for power_up in catchable_power_ups:
        power_up.remove_from_grid(grid)
        catchable_power_ups.remove(power_up)
        del power_up
    for power_up in active_power_ups:
        active_power_ups.remove(power_up)
        del power_up
    started = False
    time_limit = time + 10 * level


def move_bricks_down():
    global Bricks, game_over
    for brick in Bricks:
        brick.remove_from_grid(grid)
        brick.move_down()
        if brick.r == paddle.r-1:
            game_over = True


power_up_probability = 0.46
num_power_ups = 6
terminal_size = get_terminal_size(0)
resolution = (terminal_size.lines-3, terminal_size.columns-2)
grid = []
board = Board(resolution[0], resolution[1], grid)
board.create_grid()
Balls = []
paddle = Paddle(7, resolution[0]-2, resolution[1]//2)
Balls.append(Ball(paddle.r, paddle.c, 0, 0, grid, paddle.length, True))
lives = 3
score = 0
time = 0
catchable_power_ups = []
active_power_ups = []
game_over = False
level = 1
Bricks = generate_bricks(resolution, level)
time_limit = 0.5
time_gap = 0.1
started = False
life_lost = False
level_up_cheat = 'lL'

while not game_over:
    key = Board.display_game_details(lives, score, level, time, time_gap)
    board.print_grid()
    if key is not None and key in level_up_cheat:
        level += 1
        if level > 3:
            game_over = True
        else:
            reset_objects()
        continue
    if started:
        time += time_gap

    handle_power_ups()
    handle_balls()
    if life_lost:
        life_lost = False
        continue
    paddle.move_paddle(grid, Balls, key)
    handle_bricks()
    if check_game_over():
        level += 1
        if level > 3:
            game_over = True
        else:
            reset_objects()
            continue
    if time > time_limit and paddle.collision_ball:
        move_bricks_down()
for brick in Bricks:
    if brick.health >= 0:
        brick.remove_from_grid(grid)
        Bricks.remove(brick)
        del brick
key = Board.display_game_details(lives, score, level, time, time_gap)
board.print_grid()
print("\t\t\t\tGame Over")
