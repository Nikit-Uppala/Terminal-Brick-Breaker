from ball import Ball
from laser import Laser
import colorama
from time import sleep


class Brick:

    brick_length = 6
    colors = [None, colorama.Fore.GREEN, colorama.Fore.BLUE, colorama.Fore.RED, ""]
    color_reset = colorama.Fore.RESET

    def __init__(self, health, r, c, score):
        self.health = health
        self.r = r
        self.c = c
        self.score = score
        self.brick_structure = []
        self.ball_velocity = (-1, -1)
        for i in range(3):
            self.brick_structure.append([])
            for j in range(Brick.brick_length):
                if i == 0 or i == 2:
                    self.brick_structure[i].append(Brick.colors[self.health] + "-" + Brick.color_reset)
                else:
                    if j == 0 or j == Brick.brick_length-1:
                        self.brick_structure[i].append(Brick.colors[self.health] + "|" + Brick.color_reset)
                    else:
                        self.brick_structure[i].append(" ")

    def update_brick_structure(self):
        for i in range(3):
            for j in range(Brick.brick_length):
                if i == 1:
                    if j != 0 and j != Brick.brick_length-1:
                        self.brick_structure[i][j] = " "
                    else:
                        self.brick_structure[i][j] = Brick.colors[self.health]+"|"+Brick.color_reset
                else:
                    self.brick_structure[i][j] = Brick.colors[self.health] + "-" + Brick.color_reset

    def remove_from_grid(self, grid):
        for r in range(-1, 2):
            for c in range(Brick.brick_length):
                grid[self.r+r][self.c+c] = " "

    def move_down(self):
        self.r = self.r+1

    def update_score(self):
        return self.score

    def destroy(self, ball_velocity):
        self.health = 0
        self.ball_velocity = ball_velocity

    def on_hit(self, ball_velocity):
        if hasattr(self, "hit"):
            if not self.hit:
                self.hit = True
                return
        if self.health > 0:
            self.health -= 1
            if self.health > 0:
                self.update_brick_structure()
            else:
                self.ball_velocity = ball_velocity

    def display_on_grid(self, grid, balls, lasers):
        n_rows = len(self.brick_structure)
        start, end = -(n_rows // 2), n_rows // 2
        if grid[self.r][self.c] == Ball.symbol or grid[self.r][self.c+Brick.brick_length-1] == Ball.symbol:
            for ball in balls:
                position = ball.get_position()
                velocity = ball.get_velocity()
                if position[0] == self.r and position[1] == self.c or position[1] == self.c+Brick.brick_length:
                    ball.collision_with_horizontal_wall()
                    if hasattr(ball, "through"):
                        self.destroy(velocity)
                    else:
                        self.on_hit(velocity)
        else:
            for i in range(Brick.brick_length):
                grid[self.r][self.c+i] = self.brick_structure[1][i]
        for r in (start, end):
            for c in range(Brick.brick_length):
                if grid[self.r+r][self.c+c] == Ball.symbol:
                    for ball in balls:
                        position = ball.get_position()
                        velocity = ball.get_velocity()
                        if position[0] == self.r+r and position[1] == self.c+c:
                            if (r == start and velocity[0] < 0) or (r == end and velocity[0] > 0):
                                if velocity[1] > 0:
                                    ball.set_position(self.r, self.c, grid)
                                else:
                                    ball.set_position(self.r, self.c+Brick.brick_length-1, grid)
                                grid[self.r+r][self.c+c] = self.brick_structure[r+1][c]
                                ball.collision_with_brick_horizontal()
                            else:
                                ball.collision_with_brick_vertical()
                            if hasattr(ball, "through"):
                                self.destroy(velocity)
                            else:
                                self.on_hit(velocity)
                elif grid[self.r+r][self.c+c] == Laser.symbol:
                    velocity = (0, 0)
                    for laser in lasers:
                        if laser.r == self.r+r:
                            velocity = laser.get_velocity()
                            laser.remove_from_grid(grid)
                            lasers.remove(laser)
                            del laser
                    self.on_hit(velocity)
                else:
                    grid[self.r+r][self.c+c] = self.brick_structure[r+1][c]
        if self.health != 0:
            for r in range(-1, 2):
                grid[self.r+r][self.c] = Brick.colors[self.health]+grid[self.r+r][self.c]
                col = self.c+Brick.brick_length-1
                grid[self.r+r][col] = grid[self.r+r][col]+Brick.color_reset


class NonBreakableBrick(Brick):

    def __init__(self, r, c):
        super().__init__(-1, r, c, 100)

    def on_hit(self, velocity):
        pass

class RainbowBrick(Brick):
    
    def __init__(self, r, c):
        self.color = 0
        self.hit = False
        super().__init__(1+self.color, r, c, 75)
    
    def display_on_grid(self, grid, balls, lasers):
        if not self.hit:
            self.color = (self.color+1) % 3
            self.health = 1+self.color
            self.update_brick_structure()
        super().display_on_grid(grid, balls, lasers)

