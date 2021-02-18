from ball import Ball
import colorama


class Brick:

    brick_length = 6
    colors = [None, colorama.Fore.GREEN, colorama.Fore.BLUE, colorama.Fore.RED, ""]
    color_reset = colorama.Fore.RESET
    brick_structure = [[x for x in "------"], ["|", " ", " ", " ", " ", "|"], [x for x in "------"]]

    def __init__(self, health, r, c, score):
        self.health = health
        self.r = r
        self.c = c
        self.score = score

    def remove_from_grid(self, grid):
        for r in range(-1, 2):
            for c in range(Brick.brick_length):
                grid[self.r+r][self.c+c] = " "

    def update_score(self):
        return self.score

    def destroy(self):
        self.health = 0

    def on_hit(self):
        if self.health > 0:
            self.health -= 1

    def display_on_grid(self, grid, balls):
        n_rows = len(Brick.brick_structure)
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
                                ball.collision_with_brick_horizontal()
                                grid[self.r+r][self.c+c] = Brick.brick_structure[r+1][c]
                            else:
                                ball.collision_with_brick_vertical()
                            self.on_hit()
                elif (c == 0 or c == Brick.brick_length-1) and grid[self.r+r][self.c+c] == Ball.symbol:
                    for ball in balls:
                        position = ball.get_position()
                        if position[0] == self.r+r and position[1] == self.c+c:
                            ball.collision_with_brick_horizontal()
                            self.on_hit()
                else:
                    grid[self.r+r][self.c+c] = Brick.brick_structure[r+1][c]
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
