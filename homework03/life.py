import pathlib
import random
import typing as tp
from random import randint

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        if randomize:
            for i in range(self.rows):
                for j in range(self.cols):
                    grid[i][j] = randint(0, 1)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        neighbours = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (i, j) != (0, 0):
                    x = cell[0] + i
                    y = cell[1] + j
                    if 0 <= x < self.rows and 0 <= y < self.cols:
                        neighbours.append(self.curr_generation[x][y])
        return neighbours

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        next_generation = self.create_grid()
        for x in range(self.rows):
            for y in range(self.cols):
                n = self.get_neighbours((x, y)).count(1)
                if self.curr_generation[x][y] != 0:
                    if n in [2, 3]:
                        next_generation[x][y] = 1
                elif n == 3:
                    next_generation[x][y] = 1
        return next_generation

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if not self.is_max_generations_exceeded:
            self.prev_generation = self.curr_generation.copy()
            self.curr_generation = self.get_next_generation()
            self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations  # type: ignore

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        f = open(filename)
        height = 0
        width = 0
        grid = []
        for line in f:
            row = [int(i) for i in line if i in "01"]
            grid.append(row)
            width = len(row)
            height += 1
        life = GameOfLife((height, width), False)
        life.prev_generation = GameOfLife.create_grid(life)
        life.curr_generation = grid
        f.close()
        return life

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        f = open(filename, "w")
        for i in range(self.rows):
            for j in range(self.cols):
                f.write(str(self.curr_generation[i][j]))
            f.write("\n")
        f.close()
