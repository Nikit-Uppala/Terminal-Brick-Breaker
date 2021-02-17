from board import Board
from ball import Ball
from paddle import Paddle, GrabPaddle
from brick import Brick, NonBreakableBrick
from os import get_terminal_size
from powerup import ExpandPaddle


def handle_balls():
    global Balls, started, lives, game_over, grid, paddle
    for ball in Balls:
        if not ball.held:
            started = True
            ball.update_position(grid)
        if ball.r == len(grid)-1:
            grid[ball.r][ball.c] = "-"
            Balls.remove(ball)
            del ball
    if len(Balls) == 0:
        lives -= 1
        if lives > 0:
            Balls.append(Ball(paddle.r, paddle.c, 0, 0, paddle.length, grid, True))
        else:
            game_over = True


def handle_bricks():
    global Bricks, score
    for brick in Bricks:
        if brick.health == 0:
            brick.remove_from_grid(grid)
            Bricks.remove(brick)
            score += brick.update_score()
            del brick
        else:
            brick.display_on_grid(grid, Balls, Bricks)


def handle_power_ups():
    global catchable_power_ups, active_power_ups, grid, Balls, paddle
    for power_up in catchable_power_ups:
        if power_up.r == len(grid)-1:
            catchable_power_ups.remove(power_up)
            grid[power_up.r][power_up.c] = "-"
            del power_up
        else:
            power_up.update_position(grid, paddle, Balls, catchable_power_ups, active_power_ups)
    for power_up in active_power_ups:
        power_up.decrease_timer(time_gap)
        if power_up.time_left <= 0:
            if "=" in power_up.symbol:
                power_up.deactivate(paddle, grid)
            else:
                power_up.deactivate(Balls)
            active_power_ups.remove(power_up)
            del power_up


terminal_size = get_terminal_size(0)
resolution = (terminal_size.lines-3, terminal_size.columns//2)
grid = []
board = Board(resolution[0], resolution[1], grid)
board.create_grid()
Balls = []
Bricks = [Brick(2, 2, 15, 30)]
default_paddle = Paddle(7, resolution[0]-2, resolution[1]//2)
paddle = default_paddle
Balls.append(Ball(paddle.r, paddle.c, 0, 0, paddle.length, grid, True))
lives = 3
score = 0
time = 0
catchable_power_ups = []
active_power_ups = []
# catchable_power_ups.append()
game_over = False
time_gap = 0.06
started = False

while not game_over:
    Board.display_game_details(lives, score, time, time_gap)
    board.print_grid()
    if len(Bricks) == 0:
        game_over = True
    if started:
        time += time_gap * 2
    handle_power_ups()
    handle_balls()
    paddle.move_paddle(grid, Balls, catchable_power_ups, active_power_ups, time_gap)
    handle_bricks()
if len(Bricks) == 0:
    print("\t\t\t\t\tYou Won")
else:
    print("\t\t\t\t\tGame Over")
