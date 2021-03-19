import os
from time import sleep
from input import Get, input_to


class Board:

    def __init__(self, rows, columns, grid):
        self.rows = rows
        self.columns = columns
        self.grid = grid

    def create_grid(self):
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.columns):
                if i == 0:
                    self.grid[i].append("-")
                elif i == self.rows-1:
                    self.grid[i].append("-")
                elif j == 0 or j == self.columns - 1:
                    self.grid[i].append("|")
                else:
                    self.grid[i].append(" ")

    def print_grid(self):
        for i in range(self.rows):
            for j in range(self.columns):
                print(self.grid[i][j], end="")
            print()

    @staticmethod
    def display_game_details(lives, score, level, time, sleep_time, boss_health=None):
        get_key = Get()
        direction = input_to(get_key, sleep_time)
        if direction is not None:
            sleep(sleep_time)
        if os.name == "posix":
            os.system("clear")
        else:
            os.system("cls")
        print("Lives: %1d  Level:%1d  Time: %.1f seconds  Score: %4d  " % (lives, level, time, score), end="")
        if boss_health is not None:
            print("Boss Health: %2d"% boss_health)
        else:
            print()
        return direction
