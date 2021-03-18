import colorama


class Laser:
    symbol = colorama.Fore.RED + "^" + colorama.Fore.RESET

    def __init__(self, r, c):
        self.r, self.c = r, c
        self.v_r = -1
    
    def update_position(self, grid):
        grid[self.r][self.c] = " "
        self.r += self.v_r
        grid[self.r][self.c] = Laser.symbol
    
    def remove_from_grid(self, grid):
        if self.r == 0:
            grid[self.r][self.c] = "-"
        else:
            grid[self.r][self.c] = " "
    
    def get_velocity(self):
        return (self.v_r, 0)
