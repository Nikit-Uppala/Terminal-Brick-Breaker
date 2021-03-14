from ball import Ball
import colorama


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

    def destroy(self):
        self.health = 0

    def on_hit(self):
        if self.health > 0:
            self.health -= 1
            if self.health > 0:
                self.update_brick_structure()

    def display_on_grid(self, grid, balls):
        n_rows = len(self.brick_structure)
        start, end = -(n_rows // 2), n_rows // 2
        for r in range(start, end + 1):
            for c in range(Brick.brick_length):
                if (r == start or r == end) and grid[self.r+r][self.c+c] == Ball.symbol:
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
                            else:
                                ball.collision_with_brick_vertical()
                            if hasattr(ball, "through"):
                                self.destroy()
                            else:
                                self.on_hit()
                elif (c == 0 or c == Brick.brick_length-1) and grid[self.r+r][self.c+c] == Ball.symbol:
                    for ball in balls:
                        position = ball.get_position()
                        if position[0] == self.r+r and position[1] == self.c+c:
                            ball.collision_with_brick_horizontal()
                        if hasattr(ball, "through"):
                            self.destroy()
                        else:
                            self.on_hit()
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

    def on_hit(self):
        pass
