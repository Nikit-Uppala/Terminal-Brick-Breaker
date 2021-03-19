import colorama
from time import sleep

class Bomb:

    v_r = 1
    symbol = colorama.Fore.RED + "*" + colorama.Fore.RESET
    def __init__(self, r, c):
        self.r = r
        self.c = c
    
    def update_position(self, grid, paddle):
        grid[self.r][self.c] = " "
        self.r += Bomb.v_r
        if grid[self.r][self.c] == " ":
            grid[self.r][self.c] = Bomb.symbol
    
    def remove_from_grid(self, grid):
        if self.r == len(grid)-1:
            grid[self.r][self.c] = "-"
        grid[self.r][self.c] = " "