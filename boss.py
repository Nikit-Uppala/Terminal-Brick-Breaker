from ball import Ball
from laser import Laser
import colorama
from brick import Brick
from bomb import Bomb


class Boss:
    structure = (colorama.Fore.YELLOW + "(" + colorama.Fore.RESET,
    colorama.Fore.YELLOW + "(" + colorama.Fore.RESET,
    colorama.Fore.YELLOW + "(" + colorama.Fore.RESET,
    colorama.Fore.YELLOW + "=" + colorama.Fore.RESET,
    colorama.Fore.YELLOW + ")" + colorama.Fore.RESET,
    colorama.Fore.YELLOW + ")" + colorama.Fore.RESET,
    colorama.Fore.YELLOW + ")" + colorama.Fore.RESET
    )
    length = len(structure)
    bomb_interval = 1.2
    def __init__(self, r, c, health, time):
        self.r = r
        self.c = c
        self.health = health
        self.prev = time
        self.spawn_1 = False
        self.spawn_2 = False

    def hit(self):
        self.health -= 1

    def move_with_paddle(self, grid, paddle, balls, lasers):
        new_c = paddle.c
        diff = new_c-self.c
        if diff != 0:
            for i in range(paddle.step_size):
                if diff > 0:
                    grid[self.r][self.c+i] = " "
                else:
                    grid[self.r][self.c+Boss.length-1-i] = " "
        if new_c+Boss.length < len(grid[0])-1:
            self.c = new_c
        self.display_on_grid(grid, balls, lasers)
    
    def display_on_grid(self, grid, balls, lasers):
        for i in range(Boss.length):
            if grid[self.r][self.c+i] in (Ball.symbol, Laser.symbol):
                self.hit()
                if grid[self.r][self.c+i] == Ball.symbol:
                    for ball in balls:
                        if ball.r == self.r and ball.c == self.c+i:
                            ball.collision_with_vertical_wall()
                else:
                    for laser in lasers:
                        if laser.r == self.r and laser.c == self.c+i:
                            lasers.remove(laser)
                            del laser
            else:
                grid[self.r][self.c+i] = Boss.structure[i]
    
    def remove_from_grid(self, grid):
        for i in range(Boss.length):
            grid[self.r][self.c+i] = " "

    def pattern_1(self, bricks, resolution):
        self.spawn_1 = True
        bricks.append(Brick(3, 9, 4, 50))
        bricks.append(Brick(1, 9, 12, 10))
        bricks.append(Brick(2, 9, 20, 30))

    def pattern_2(self, bricks, resolution):
        self.spawn_2 = True
        bricks.append(Brick(3, 13, 4, 50))
        bricks.append(Brick(1, 13, 12, 10))
        bricks.append(Brick(2, 13, 20, 30))
    
    def generate_bomb(self, bombs):
        bombs.append(Bomb(self.r, self.c+Boss.length//2))

